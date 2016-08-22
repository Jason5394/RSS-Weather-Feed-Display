import menu_view as mv
import weather_model as model
import weather_parser as wp
import tkinter as tk
from pubsub import pub

class MenuController:
    '''Controller for menu items and their respective toplevels'''
    def __init__(self, root):
        