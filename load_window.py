import tkinter as tk
import weather_view as view
from pubsub import pub

class LoadWindow(view.FormTopLevel):
    def __init__(self, root, **kwargs):
        view.FormTopLevel.__init(self, root, **kwargs)
        #get loaded data
        