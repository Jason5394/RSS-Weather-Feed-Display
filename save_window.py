import weather_view as view
from pubsub import pub
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

class SaveWindow(view.FormTopLevel):
    '''Window that appears when user chooses "Save" in menu dropdown.'''
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        pub.subscribe(self.invalidSave, "invalidSave")
        pub.subscribe(self.validSave, "validSave")
        self.weatherdict = self.root.model.getWeatherDict()
        self.error_toplevel = None
        self.root = root
        default_entry = ""
        if self.weatherdict:
            if self.weatherdict["url"]:
                default_entry = self.weatherdict["url"]
        
        #construct inner frames
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0)
        self.frame2 = ttk.Frame(self)
        self.frame2.grid(column=0, row=1)
        #create widgets
        self.instruct_label = ttk.Label(self.frame1, text="Save an RSS feed")
        self.name_label = ttk.Label(self.frame1, text="RSS name:")
        self.url_label = ttk.Label(self.frame1, text="RSS feed URL:")
        self.url_entry = ttk.Entry(self.frame1, width=50)
        self.url_entry.insert(0, default_entry)
        self.name_entry = ttk.Entry(self.frame1, width=50)
        self.submit_button = ttk.Button(self.frame2, text="Save", width=10, command=self.pressedSave)
        self.cancel_button = ttk.Button(self.frame2, text="Cancel", width=10, command=self.pressedCancel)
        #place widgets
        self.instruct_label.grid(column=0, row=0, columnspan=2)
        self.name_label.grid(column=0, row=1, sticky=tk.E)
        self.name_entry.grid(column=1, row=1)
        self.url_label.grid(column=0, row=2, sticky=tk.E)
        self.url_entry.grid(column=1, row=2)
        self.submit_button.grid(column=0, row=0)
        self.cancel_button.grid(column=1, row=0)
       
    def pressedCancel(self):
        self.unsubscribe()
        self.root.removeTopLevel("save")
        
    def pressedSave(self):
        url = self.url_entry.get()
        name = self.name_entry.get()
        self.root.model.addSavedUrl(url, name)
        
    def invalidSave(self, message):
        self.error_toplevel = tkinter.messagebox.showerror("Error", message, parent=self)
        
    def validSave(self):
        self.unsubscribe()
        self.root.removeTopLevel("save")
        
    def unsubscribe(self):
        pub.unsubscribe(self.invalidSave, "invalidSave")
        pub.unsubscribe(self.validSave, "validSave")
        