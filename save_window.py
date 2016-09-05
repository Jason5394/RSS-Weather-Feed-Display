import weather_view as view
from pubsub import pub
import tkinter as tk
import tkinter.messagebox

class SaveWindow(view.FormTopLevel):
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        pub.subscribe(self.invalidSave, "invalidSave")
        pub.subscribe(self.validSave, "validSave")
        self.weatherdict = self.root.model.getWeatherDict()
        self.error_toplevel = None
        self.root = root
        default_entry = ""
        print (self.weatherdict)
        if self.weatherdict:
            default_entry = self.weatherdict["url"]
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
        