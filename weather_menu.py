import tkinter as tk
import tkinter.messagebox
import weather_view as view
import error_message as em
from pubsub import pub


class AppMenu(tk.Menu):
    def __init__(self, master, model, **kwargs): #see if this can be changed 
        tk.Menu.__init__(self, master, **kwargs)
        self.weatherdict = {}
        self.model = model
        self.toplevels = {"load": None, "save": None, "help": None, "about": None}
        
        #filemenu, which has load, save and exit buttons
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Load", command=self.loadSavedUrls)
        self.filemenu.add_command(label="Save", command=self.saveUrl)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.master.quit)
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
        
    def initTopLevel(self, key, Class, *args):
        if self.toplevels[key] is None:
            print("making toplevel:", Class)
            self.toplevels[key] = Class(self, *args)
            self.toplevels[key].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel(key))
            return True
        return False
        
    def loadSavedUrls(self):
        print("filemenu button: load")
        if self.initTopLevel("load", LoadWindow):
            pass
        
    def saveUrl(self):
        # print("filemenu button: save")
        # if self.initTopLevel("save", SaveWindow, self.weatherdict):
            # print("True")
        # else:
            # print("False")'
    
        if self.toplevels["save"] is None:
            print("making toplevel: save")
            self.toplevels["save"] = SaveWindow(self, self.weatherdict)
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

   
class LoadWindow(view.FormTopLevel):
    pass
    
    
class SaveWindow(view.FormTopLevel):
    def __init__(self, root, weatherdict, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        pub.subscribe(self.invalidSave, "invalidSave")
        pub.subscribe(self.validSave, "validSave")
        self.error_toplevel = None
        self.root = root
        default_entry = ""
        print (weatherdict)
        if weatherdict:
            default_entry = weatherdict["url"]
            print("url:", default_entry)
        
        self.frame.config(padx=4)
        
        #construct second frame
        self.frame2 = tk.Frame(self, padx=2, pady=2)
        self.frame2.grid(column=0, row=1)
        
        self.instruct_label = tk.Label(self.frame, text="Save an RSS feed")
        self.name_label = tk.Label(self.frame, text="RSS name:")
        self.url_label = tk.Label(self.frame, text="RSS feed URL:")
        self.submit_button = tk.Button(self.frame2, text="Save", width=10, command=self.pressedSave)
        self.cancel_button = tk.Button(self.frame2, text="Cancel", width=10, command=self.pressedCancel)
        self.url_entry = tk.Entry(self.frame, width=50)
        self.url_entry.insert(0, default_entry)
        self.name_entry = tk.Entry(self.frame, width=50)
        
        self.instruct_label.grid(column=0, row=0, columnspan=2)
        self.name_label.grid(column=0, row=1, sticky=tk.E)
        self.name_entry.grid(column=1, row=1)
        self.url_label.grid(column=0, row=2, sticky=tk.E)
        self.url_entry.grid(column=1, row=2)
        self.submit_button.grid(column=0, row=0, sticky=tk.W+tk.E)
        self.cancel_button.grid(column=1, row=0, sticky=tk.W+tk.E)
       
    def pressedCancel(self):
        self.root.removeTopLevel("save")
        
    def pressedSave(self):
        url = self.url_entry.get()
        name = self.name_entry.get()
        self.root.model.addSavedUrl(url, name)
        
    def invalidSave(self, message):
        #if self.error_toplevel is None:
        self.error_toplevel = tkinter.messagebox.showerror("Error", message, parent=self.root.toplevels["save"])
        #self.error_toplevel.protocol("WM_DELETE_WINDOW", self.removeErrorTopLevel)
    
    def removeErrorTopLevel(self):
        self.error_toplevel.destroy()
        self.error_toplevel = None
        
    def validSave(self):
        self.root.removeTopLevel("save")

        
        
        
       
    

class AboutWindow(view.FormTopLevel):
    pass
    
    
def main():
    root = tk.Tk()
    appMenu = AppMenu(root)
    root.config(menu=appMenu)
    root.mainloop()
    
if __name__ == '__main__': main()