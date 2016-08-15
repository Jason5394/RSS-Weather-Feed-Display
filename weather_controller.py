import weather_model as model
import weather_view as view
import weather_parser as wp
import tkinter as tk
from tkinter import ttk
from pubsub import pub

class WeatherController:
    '''
    Controller in the MVC for the application.
    '''
    def __init__(self, root):
        url = self.getMostRecentUrl()
       
        self.model = model.WeatherModel()
        pub.subscribe(self.valuesChanged, "valuesChanged")
        self.mainframe = view.WeatherView(root)
        self.mainframe.refresh_button.config(command=self.updateValues)
        self.mainframe.change_rss_button.config(command=self.changeRSS)
        
    def getMostRecentUrl(self):
        #retrieves most recently used url from a file somewhere 
        return None
    
    def valuesChanged(self, url):
        '''Listener that changes the weather data in the application'''
        weatherObj = wp.WeatherData(url)
        self.mainframe.setValues(weatherObj)
        
    def updateValues(self):
        url = self.model.getUrl()
        self.model.setWeather(url)
        
    def changeRSS(self):
        print("attempting to change rss feed")
        if self.mainframe.toplevel_1 is None:
            self.mainframe.toplevel_1 = view.ChangeRSSWindow(self.mainframe)
            self.mainframe.toplevel_1.submit_rss_button.config(command=self.pressedSubmit)
            self.mainframe.toplevel_1.protocol("WM_DELETE_WINDOW", self.removeTopLevel_1)
            
    def removeTopLevel_1(self):
        self.mainframe.toplevel_1.destroy()
        self.mainframe.toplevel_1 = None
        
    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.mainframe.toplevel_1.rssEntry.get()
        print("RSS feed:", rss)
        if wp.WeatherData.isValidRSS(rss) is True:
            self.model.setWeather(rss)
            self.mainframe.toplevel_1.destroy()
            self.mainframe.toplevel_1 = None
        else:
            print("invalid url")
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    controller = WeatherController(root)
    root.mainloop()
    
    
if __name__ == "__main__": main()