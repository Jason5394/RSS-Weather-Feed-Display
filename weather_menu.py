import tkinter as tk
import tkinter.messagebox
import weather_view as view
import error_message as em
from save_window import *
from load_window import *
from pubsub import pub


class AppMenu(tk.Menu):
    def __init__(self, root, controller, **kwargs): #see if this can be changed 
        tk.Menu.__init__(self, root, **kwargs)
        self.weatherdict = {}
        self.controller = controller
        self.model = self.controller.model
        self.root = root
        self.toplevels = {"load": None, "save": None, "help": None, "about": None}
        
        #filemenu, which has load, save and exit buttons
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Load", command=self.loadSavedUrls)
        self.filemenu.add_command(label="Save", command=self.saveUrl)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.add_cascade(label="File", menu=self.filemenu)
        
        #helpmenu, which has help and about buttons
        self.helpmenu = tk.Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.showInstructions)
        self.helpmenu.add_command(label="About", command=self.showAbout)
        self.add_cascade(label="Help", menu=self.helpmenu)    
        
    def setValues(self, weatherdict):
        self.weatherdict = weatherdict
    
    def removeTopLevel(self, key):
        print("key:", key)
        '''function called when window that changes rss feed is destroyed.'''
        self.toplevels[key].destroy()
        self.toplevels[key] = None 
                
    def loadSavedUrls(self):
        if self.toplevels["load"] is None:
            self.toplevels["load"] = LoadWindow(self)
            self.toplevels["load"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("load"))
        
    def saveUrl(self):
        if self.toplevels["save"] is None:
            self.toplevels["save"] = SaveWindow(self)
            self.toplevels["save"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("save"))
        
    def showInstructions(self):
        print("helpmenu button: help")
        if self.initTopLevel("help", InstructionsWindow):
            pass
            
    def showAbout(self):
        print("helpmenu button: about")
        if self.initTopLevel("about", AboutWindow):
            pass
        
class InstructionsWindow(view.FormTopLevel):
    def __init__():
        pass

class AboutWindow(view.FormTopLevel):
    pass
    
    
def main():
    root = tk.Tk()
    appMenu = AppMenu(root)
    root.config(menu=appMenu)
    root.mainloop()
    
if __name__ == '__main__': main()