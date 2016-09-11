import tkinter as tk
import tkinter.messagebox
import weather_view as view
import webbrowser
from save_window import *
from load_window import *
from pubsub import pub


class AppMenu(tk.Menu):
    '''Menu class that generates the dropdown menu for the app'''

    def __init__(self, root, ctrler, **kwargs):  # see if this can be changed
        tk.Menu.__init__(self, root, **kwargs)
        self.weatherdict = {}
        self.ctrler = ctrler
        self.model = self.ctrler.model
        self.root = root
        self.toplevels = {"load": None, "save": None,
                          "help": None, "about": None}

        # filemenu, which has load, save and exit buttons
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Load", command=self.loadSavedUrls)
        self.filemenu.add_command(label="Save", command=self.saveUrl)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.add_cascade(label="File", menu=self.filemenu)

        # helpmenu, which has help and about buttons
        self.helpmenu = tk.Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.showInstructions)
        self.helpmenu.add_command(label="About", command=self.showAbout)
        self.add_cascade(label="Help", menu=self.helpmenu)

    def setValues(self, weatherdict):
        self.weatherdict = weatherdict

    def removeTopLevel(self, key):
        print("key:", key)
        '''function called when window that changes rss feed is destroyed.'''
        self.ctrler.toplevels[key].destroy()
        self.ctrler.toplevels[key] = None

    def loadSavedUrls(self):
        if not self.ctrler.toplevels["load"]:
            self.ctrler.toplevels["load"] = LoadWindow(self.root, self.ctrler,
                                                       title="Load/Delete Saved Feed")

    def saveUrl(self):
        if not self.ctrler.toplevels["save"]:
            self.ctrler.toplevels["save"] = SaveWindow(self.root, self.ctrler,
                                                       title="Save RSS Feed")

    def showInstructions(self):
        if not self.toplevels["help"]:
            self.ctrler.toplevels["help"] = InstructionsWindow(self.root,
                                                               title="Help")
            self.ctrler.toplevels["help"].protocol("WM_DELETE_WINDOW",
                                                   lambda: self.ctrler.removeTopLevel("help"))

    def showAbout(self):
        if not self.toplevels["about"]:
            self.ctrler.toplevels["about"] = AboutWindow(self.root,
                                                         title="About")
            self.ctrler.toplevels["about"].protocol("WM_DELETE_WINDOW",
                                                    lambda: self.ctrler.removeTopLevel("about"))


class InstructionsWindow(view.FormTopLevel):

    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        self.frame.config(padding=6)

        self.homepage = "http://w1.weather.gov/xml/current_obs/seek.php"
        instructions = ("This weather app only serves the NOAA's National Weather Service "
                        "RSS feed. To choose a weather feed, click on the website below. Navigate to "
                        "your desired weather RSS feed and copy the url. "
                        "Click on the Change feed button and paste the url. The "
                        "corresponding weather information should populate the window. \n\n"

                        "By pressing on the Show source button, you can view your RSS feed in its raw "
                        "form. Pressing Update attempts to retrieve updates from the current feed and displays "
                        "the newly changed results on the screen. \n\n"

                        "You can also save feeds by clicking on the File menu and then Save. Load the saved "
                        "feed by pressing Load and choosing from your saved feeds.")

        self.instruct_text = tk.Text(self.frame, wrap=tk.WORD,
                                     height=12, width=60, font="Calibri")
        self.instruct_text.insert(tk.END, instructions)
        self.instruct_text.config(state=tk.DISABLED)
        self.instruct_text.grid(column=0, row=0)

        self.link = ttk.Label(self.frame, text=self.homepage,
                              font="Calibri", foreground="blue", cursor="hand2")
        self.link.bind("<Button-1>", self.gotoHomepage)
        self.link.grid(column=0, row=1)

    def gotoHomepage(self, event):
        print("Going to homepage")
        webbrowser.open_new(self.homepage)

    def setCursorType(self, event, type="left_ptr"):
        print(type)
        self.instruct_text.config(cursor=type)


class AboutWindow(view.FormTopLevel):

    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        self.frame.config(padding=6)
        about = ("This app was created by Jason Yang, 2016. The National Oceanic and "
                 "Atmospheric Administrations' National Weather Service was the main resource used to pull "
                 "weather information as RSS feeds. All weather parsing and weather data types closely "
                 "model that of the aforementioned feed.")

        about_text = tk.Text(self.frame, wrap=tk.WORD,
                             height=5, width=60, font="Calibri")
        about_text.insert(tk.END, about)
        about_text.config(state=tk.DISABLED)
        about_text.grid(column=0, row=0)


def main():
    root = tk.Tk()
    appMenu = AppMenu(root)
    root.config(menu=appMenu)
    root.mainloop()

if __name__ == '__main__':
    main()
