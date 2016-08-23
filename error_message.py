import weather_view as view
import tkinter as tk

class ErrorMessage(view.FormTopLevel):
    def __init__(self, root, message, action, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        #print("message:", message, "action:", action)
        self.action = action
        okay_button = tk.Button(self.frame, text="OK", command=action)
        self.frame.bind("<Return>", self.doAction)
        message_label = tk.Label(self.frame, text=message)
        message_label.grid(column=0, row=0)
        okay_button.grid(column=0, row=1)
        
    def doAction(self, event):
        self.action()
        
        