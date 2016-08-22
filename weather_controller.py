import weather_model as model
import weather_menu as wm
import weather_view as view
import weather_parser as wp
import tkinter as tk
from pubsub import pub

class WeatherController:
    '''
    Controller in the MVC for the application.
    '''
    def __init__(self, root):
        url = self.getMostRecentUrl()
        self.root = root
        self.model = model.WeatherModel()
        pub.subscribe(self.valuesChanged, "valuesChanged")
        self.mainframe = view.WeatherView(root)
        self.mainframe.refresh_button.config(command=self.pressedUpdate)
        self.mainframe.change_rss_button.config(command=self.pressedChangeRss)
        self.mainframe.show_src_button.config(command=self.pressedShowSrc)
        
        self.menuApp = wm.AppMenu(self.mainframe, self.model)
        self.root.config(menu=self.menuApp)
        
    def getMostRecentUrl(self):
        #retrieves most recently used url from a file somewhere 
        return None
    
    def valuesChanged(self, weather_dict):
        '''Listener that changes the weather data in the application'''
        #weatherObj = wp.WeatherData(url)
        self.mainframe.setValues(weather_dict)
        self.menuApp.setValues(weather_dict)
        
    def pressedUpdate(self):
        weatherdict = self.model.getWeatherDict()
        if weatherdict is not None:
            self.model.setWeather(weatherdict["url"])
        
    def pressedChangeRss(self):
        print("attempting to change rss feed")
        if self.mainframe.toplevels["changeRSS"] is None:
            self.mainframe.toplevels["changeRSS"] = view.ChangeRSSWindow(self.mainframe)
            self.mainframe.toplevels["changeRSS"].submit_rss_button.config(command=self.pressedSubmit)
            self.mainframe.toplevels["changeRSS"].rss_entry.bind("<Return>", self.pressedReturnHandler)
            self.mainframe.toplevels["changeRSS"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("changeRSS"))
    
    def pressedReturnHandler(self, event):
        self.pressedSubmit()
        
    def removeTopLevel(self, key):
        '''function called when window that changes rss feed is destroyed.'''
        self.mainframe.toplevels[key].destroy()
        self.mainframe.toplevels[key] = None
        
    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.mainframe.toplevels["changeRSS"].rss_entry.get()
        print("RSS feed:", rss)
        if wp.WeatherData.isValidRSS(rss) is True:
            self.model.setWeather(rss)
            self.removeTopLevel("changeRSS")
        else:
            print("invalid url")
            
    def pressedShowSrc(self):
        if self.mainframe.toplevels["showFeed"] is None:
            weatherdict = self.model.getWeatherDict()
            if weatherdict is not None:
                self.mainframe.toplevels["showFeed"] = view.ShowSourceWindow(self.mainframe)
                self.mainframe.toplevels["showFeed"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("showFeed"))
                self.mainframe.toplevels["showFeed"].setSrc(weatherdict["rss_feed"])
            
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    controller = WeatherController(root)
    root.mainloop()
     
if __name__ == "__main__": main()