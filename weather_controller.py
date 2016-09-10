import weather_model as model
import weather_menu as wm
import weather_view as view
import weather_parser as wp
import tkinter as tk
import tkinter.messagebox
from pubsub import pub

class WeatherController:
    '''
    Controller in the MVC for the application.
    '''
    def __init__(self, root):
        self.root = root
        self.model = model.WeatherModel()
        url = self.getMostRecentUrl()
        
        self.toplevels = {"changeRSS": None,
                            "showFeed": None,
                            "load": None,
                            "save": None,
                            "help": None,
                            "about": None}
                            
        self.mainframe = view.WeatherView(root)
        self.mainframe.refresh_button.config(command=self.pressedUpdate)
        self.mainframe.change_rss_button.config(command=self.pressedChangeRss)
        self.mainframe.show_src_button.config(command=self.pressedShowSrc)
        
        self.menuApp = wm.AppMenu(self.mainframe, self)
        self.root.config(menu=self.menuApp)
        
        pub.subscribe(self.valuesChanged, "valuesChanged")
        
        self.model.setWeather(url)
        
    def getMostRecentUrl(self):
        '''retrieves most recently used url from the pickle file '''
        return self.model.getUrl()
    
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
        if self.toplevels["changeRSS"] is None:
            self.toplevels["changeRSS"] = view.ChangeRSSWindow(self.mainframe)
            self.toplevels["changeRSS"].submit_rss_button.config(command=self.pressedSubmit)
            self.toplevels["changeRSS"].rss_entry.bind("<Return>", self.pressedReturnHandler)
            self.toplevels["changeRSS"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("changeRSS"))
    
    def pressedReturnHandler(self, event):
        self.pressedSubmit()
        
    def removeTopLevel(self, key):
        '''function called when window that changes rss feed is destroyed.'''
        self.toplevels[key].destroy()
        self.toplevels[key] = None
        
    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.toplevels["changeRSS"].rss_entry.get()
        print("RSS feed:", rss)
        if wp.WeatherData.isValidRSS(rss):
            self.model.setWeather(rss)
            self.removeTopLevel("changeRSS")
        else:
            print("invalid url")
            self.error_message = tkinter.messagebox.showerror("Error", "RSS feed is invalid.", parent=self.toplevels["changeRSS"])
                      
    def pressedShowSrc(self):
        if self.toplevels["showFeed"] is None:
            weatherdict = self.model.getWeatherDict()
            if weatherdict["rss_feed"]:
                self.toplevels["showFeed"] = view.ShowSourceWindow(self.mainframe, weatherdict["rss_feed"])
                self.toplevels["showFeed"].protocol("WM_DELETE_WINDOW", lambda: self.removeTopLevel("showFeed"))
            
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    controller = WeatherController(root)
    root.mainloop()
     
if __name__ == "__main__": main()