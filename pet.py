import tkinter as tk
import time
import random
from win32api import GetMonitorInfo, MonitorFromPoint
class pet():
    
    def __init__(self):

        self.winSize = '128x128+{x}+{y}';
        #Intitial window setup
        self.window = tk.Tk();
        screenWidth = (self.window.winfo_screenwidth());
        
        self.action = 0;
        self.flip = False;

        self.idle = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % (i)) for i in range(2)];
        self.idleFlip = [tk.PhotoImage(file='idleFlip.gif', format='gif -index %i' % (i)) for i in range(2)];
        self.walking_right = [tk.PhotoImage(file='walking_right.gif', format='gif -index %i' % (i)) for i in range(3)];
        self.walking_left = [tk.PhotoImage(file='walking_left.gif', format='gif -index %i' % (i)) for i in range(3)];
        self.frame_index = 0
        self.img = self.idle[self.frame_index]
        self.timestamp = time.time()
        
        self.window.config(highlightbackground='lime');
        self.window.overrideredirect(True);
        self.window.attributes('-topmost',True);
        self.window.wm_attributes('-transparentcolor','lime');
        self.label = tk.Label(self.window,bd=0,bg='lime');
        self.x = int(screenWidth/2);
        self.y = self.window.winfo_screenheight() - (128+(self.getTaskbarHeight()));
        self.window.geometry(self.winSize.format(x=str(self.x),y=str(self.y)));
        self.label.configure(image=self.img);
        self.label.pack();
        self.window.after(0, self.update);
        self.window.after(0, self.newAction);
        self.window.mainloop();

    def getTaskbarHeight(self):
        monInfo = GetMonitorInfo(MonitorFromPoint((0,0)));
        monArea = monInfo.get("Monitor");
        workArea = monInfo.get("Work");
        return (monArea[3] - workArea[3]);

    def noMove(self):
        # advance frame if 200ms have passed
        if time.time() > self.timestamp + 0.2:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % len(self.idle)

            if (self.flip):
                self.img = self.idleFlip[self.frame_index]
            else:
                self.img = self.idle[self.frame_index]

        # create the window
        self.window.geometry(self.winSize.format(x=str(self.x),y=str(self.y)));
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        return;

    def moveRight(self):

        self.flip = True;
        
        if (self.x >= (self.window.winfo_screenwidth() - 128)):
            self.newAction();
            
        # move right by one pixel
        self.x += 1

        # advance frame if 200ms have passed
        if time.time() > self.timestamp + 0.2:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % len(self.walking_right)
            self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry(self.winSize.format(x=str(self.x),y=str(self.y)));
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        return;

    def moveLeft(self):

        self.flip = False;
        
        if (self.x <= 0):
            self.newAction();
            
        # move right by one pixel
        self.x -= 1

        # advance frame if 200ms have passed
        if time.time() > self.timestamp + 0.2:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % len(self.walking_left)
            self.img = self.walking_left[self.frame_index]

        # create the window
        self.window.geometry(self.winSize.format(x=str(self.x),y=str(self.y)));
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        return;

    def newAction(self):
        self.action = (random.randrange(0,4));
        self.window.after(1000, self.newAction);

    def update(self):

        if (self.action == 0):
            self.moveLeft();
        elif (self.action == 1):
            self.moveRight();
        else:
            self.noMove();
        
        self.window.after(10, self.update);


pet();
