import tkinter as tk
import weather_controller as wc

class AppMenu(tk.Menu):
    def __init__(self, master, **kwargs):
        tk.Menu.__init__(self, master, **kwargs)
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
        
    def loadSavedUrls(self):
        print("filemenu button: load")
        
    def saveUrl(self):
        print("filemenu button: save")
        
    def showInstructions(self):
        print("helpmenu button: help")
        
    def showAbout(self):
        print("helpmenu button: about")
        
def main():
    root = tk.Tk()
    appMenu = AppMenu(root)
    root.config(menu=appMenu)
    root.mainloop()
    
if __name__ == '__main__': main()