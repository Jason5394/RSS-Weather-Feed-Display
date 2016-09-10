import tkinter as tk
import tkinter.ttk as ttk
import weather_view as view
from pubsub import pub

class LoadWindow(view.FormTopLevel):
    '''Window that pops up after user presses "Load" in menu dropdown'''
    def __init__(self, root, controller=None, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.__pressedCancel)
        
        #get loaded data
        self.saved_urls = controller.model.getSavedUrls()
        self.saved_names = controller.model.getSavedNames()
        self.root = root
        self.ctrler = controller
        
        #create gui frames
        self.resizable(0,0)
        self.frame1 = ttk.Frame(self.frame, padding=2)
        self.frame2 = ttk.Frame(self.frame, padding=2)
        self.frame3 = ttk.Frame(self.frame, padding=2)
        self.frame1.grid(column=0, row=0)
        self.frame2.grid(column=0, row=1)
        self.frame3.grid(column=0, row=2)
        self.instruct_label = ttk.Label(self.frame1, text="Load a previously saved RSS feed.")
        self.instruct_label.grid(column=0, row=0)
        
        #add treeview headers
        self.tree = ttk.Treeview(self.frame2)
        self.tree["columns"] = ("rssfeedurl")
        self.tree.heading("#0", text="Name")
        self.tree.heading("rssfeedurl", text="RSS feed url")
        self.tree.column("#0", minwidth=0, width=150)
        self.tree.column("rssfeedurl", minwidth=0, width=300)
        vsb = ttk.Scrollbar(self.frame2, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame2, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(sticky=(tk.N,tk.S,tk.W,tk.E), column=0, row=0)
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        #add buttons
        self.load_button = ttk.Button(self.frame3, text="Load", width=10, command=self.__pressedLoad)
        self.delete_button = ttk.Button(self.frame3, text="Delete", width=10, command=self.__pressedDelete)
        self.cancel_button = ttk.Button(self.frame3, text="Cancel", width=10, command=self.__pressedCancel)
        self.load_button.grid(column=0, row=0)
        self.delete_button.grid(column=1, row=0)
        self.cancel_button.grid(column=2, row=0)
        
        self.__initList()
        
    def __initList(self):
        for name, url in zip(self.saved_names, self.saved_urls):
            self.tree.insert("", "end", text=name, values=(url))
    
    def __updateValues(self):
        '''saves the current list of values in tree view to the model, and
        subsequently to pickle file'''
        names = []
        urls = []
        for child in self.tree.get_children():
            #add names and urls from tree to temporary list
            names.append(self.tree.item(child)["text"])
            urls.append(self.tree.item(child)["values"][0])
        self.ctrler.model.setSavedLists(names, urls)
        
    def __pressedLoad(self):
        self.__updateValues()
        current_item = self.tree.focus()
        if current_item:
            url = self.tree.item(current_item)["values"][0]
            self.ctrler.model.setWeather(url)
        self.ctrler.removeTopLevel("load")
            
    def __pressedDelete(self):
        current_item = self.tree.focus()
        if current_item:
            self.tree.delete(current_item)
            
    def __pressedCancel(self):
        self.__updateValues()
        self.ctrler.removeTopLevel("load")
        
       