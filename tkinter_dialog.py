#   Source code for FormTopLevel class taken
#   from effbot.org/tkinterbook/tkinter-dialog-windows.htm
#   and modified to fit the application.
#   Used in this application to create custom dialog windows

import tkinter as tk

class FormTopLevel(tk.Toplevel):

    def __init__(self, root, title=None, resizeable=False, **kwargs):

        tk.Toplevel.__init__(self, root, **kwargs)
        self.transient(root)
        self.root = root
        if title:
            self.title(title) 
        if resizeable:
            self.resizeable(0,0)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))
                                  
        self.frame = tk.Frame(self)   
        self.frame.grid(column=0, row=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.wait_window(self)

    def cancel(self, event=None):
        self.root.focus_set()
        self.destroy()
