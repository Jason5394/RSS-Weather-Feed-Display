import weather_view as view
import tkinter as tk

class ErrorMessage(view.FormTopLevel):
    def __init__(self, root, message, action=None, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        #print("message:", message, "action:", action)
        self.root = root
        self.action = action
        self.grab_set()
        self.geometry("+%d+%d" % (self.root.winfo_rootx()+50,
                                  self.root.winfo_rooty()+50))
        okay_button = tk.Button(self.frame, text="OK", command=self.destroy)
        self.frame.bind("<Return>", self.doAction)
        message_label = tk.Label(self.frame, text=message)
        message_label.grid(column=0, row=0)
        okay_button.grid(column=0, row=1)
        
        self.wait_window(self)
    def doAction(self, event):
        self.destroy()()
        
        