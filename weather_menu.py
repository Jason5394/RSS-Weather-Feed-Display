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
        if not self.toplevels["load"]:
            self.toplevels["load"] = LoadWindow(self)
            self.toplevels["load"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("load"))
        
    def saveUrl(self):
        if not self.toplevels["save"]:
            self.toplevels["save"] = SaveWindow(self)
            self.toplevels["save"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("save"))
        
    def showInstructions(self):
        if not self.toplevels["help"]:
            self.toplevels["help"] = InstructionsWindow(self)
            self.toplevels["help"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("help"))
                
    def showAbout(self):
        if not self.toplevels["about"]:
            self.toplevels["about"] = AboutWindow(self)
            self.toplevels["about"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("about"))
        
class InstructionsWindow(view.FormTopLevel):
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        
        instructions = ("This weather app only serves the NOAA's National Weather Service "
        "RSS feed.  To choose a weather feed, go to http://w1.weather.gov/xml/current_obs/seek.php "
        "and copy the url.  Click on the \"Change feed\" button and enter the url.  The "
        "correct weather information should populate. \n\n"
            
        "By pressing on the \"Show source\" button, you can view your RSS feed in its raw "
        "form.  Pressing \"Update\" attempts to retrieve updates from the current feed and displays "
        "the newly changed results on the screen. \n\n"
            
        "You can also save feeds by clicking on the File menu and then Save.  Load the saved "
        "feed by pressing \"Load\" and choosing from your saved feeds.")
        
        instruct_msg = tk.Message(self.frame, text=instructions, padx=10, pady=10, 
                                    justify=tk.LEFT, width=400)
        instruct_msg.grid(column=0, row=0)

class AboutWindow(view.FormTopLevel):
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        
        about = ("This app was created by Jason Yang, 2016. The National Oceanic and "
            "Atmospheric Administrations' National Weather Service was the main resource used to pull " 
            "weather information as RSS feeds. All weather parsing and weather data types closely " 
            "model that of the aforementioned feed.")
        
        about_msg = tk.Message(self.frame, text=about, justify = tk.LEFT,
                                width=400, padx=10, pady=10)
        about_msg.grid(column=0, row=0)
    
    
def main():
    root = tk.Tk()
    appMenu = AppMenu(root)
    root.config(menu=appMenu)
    root.mainloop()
    
if __name__ == '__main__': main()