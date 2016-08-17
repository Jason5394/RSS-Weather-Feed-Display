import weather_model as model
import weather_view as view
import menu
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
        self.mainframe.refresh_button.config(command=self.pressedUpdate)
        self.mainframe.change_rss_button.config(command=self.pressedChangeRss)
        self.mainframe.show_src_button.config(command=self.pressedShowSrc)
        
    def getMostRecentUrl(self):
        #retrieves most recently used url from a file somewhere 
        return None
    
    def valuesChanged(self, url):
        '''Listener that changes the weather data in the application'''
        weatherObj = wp.WeatherData(url)
        self.mainframe.setValues(weatherObj)
        
    def pressedUpdate(self):
        weatherObj = self.model.getWeatherObj()
        if weatherObj is not None:
            self.mainframe.setValues(weatherObj)
        
    def pressedChangeRss(self):
        print("attempting to change rss feed")
        if self.mainframe.toplevel_1 is None:
            self.mainframe.toplevel_1 = view.ChangeRSSWindow(self.mainframe)
            self.mainframe.toplevel_1.submit_rss_button.config(command=self.pressedSubmit)
            self.mainframe.toplevel_1.rss_entry.bind("<Return>", self.pressedReturnHandler)
            self.mainframe.toplevel_1.protocol("WM_DELETE_WINDOW", self.removeTopLevel_1)
    
    def pressedReturnHandler(self, event):
        self.pressedSubmit()
        
    def removeTopLevel_1(self):
        '''function called when window that changes rss feed is destroyed.'''
        self.mainframe.toplevel_1.destroy()
        self.mainframe.toplevel_1 = None
    
    def removeTopLevel_2(self):
        '''function called when window that displays rss source is destroyed.'''
        self.mainframe.toplevel_2.destroy()
        self.mainframe.toplevel_2 = None
        
    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.mainframe.toplevel_1.rss_entry.get()
        print("RSS feed:", rss)
        if wp.WeatherData.isValidRSS(rss) is True:
            self.model.setWeather(rss)
            self.mainframe.toplevel_1.destroy()
            self.mainframe.toplevel_1 = None
        else:
            print("invalid url")
            
    def pressedShowSrc(self):
        if self.mainframe.toplevel_2 is None:
            weatherObj = self.model.getWeatherObj()
            if weatherObj is not None:
                self.mainframe.toplevel_2 = view.ShowSourceWindow(self.mainframe)
                self.mainframe.toplevel_2.protocol("WM_DELETE_WINDOW", self.removeTopLevel_2)
                self.mainframe.toplevel_2.setSrc(weatherObj.rss_feed)
            
        
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    controller = WeatherController(root)
    root.mainloop()
     
if __name__ == "__main__": main()