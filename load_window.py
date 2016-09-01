import tkinter as tk
import weather_view as view
from pubsub import pub

class LoadWindow(view.FormTopLevel):
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init__(self, root, **kwargs)
        #get loaded data
        self.saved_urls = self.root.model.getSavedUrls()
        self.saved_names = self.root.model.getSavedNames()
        