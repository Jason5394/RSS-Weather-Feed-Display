import weather_parser as wp
import tkinter as tk
from tkinter import ttk

class WeatherDisplay:
    '''Application to display weather from an RSS feed.'''
    
    def refreshData(self):
        print("refreshing data from rss")
        try:
            self.weatherData = wp.WeatherData(self.url)
        except weather_parser.invalidUrl:
            self.weatherData = None
        self.weatherData.display()
        self.setValues()
        self.root.update()
    
    def changeRSS(self):
        print("attempting to change rss feed")
        if self.toplevel is None:
            self.toplevel = ChangeRSSWindow(self.root, self)
            self.toplevel.protocol("WM_DELETE_WINDOW", self.removeTopLevel)
             
    def getTopLevelRSS(self, url):
        if url is not None:
            self.url = url
            print("new url:", url)
            self.refreshData()
        
    def removeTopLevel(self):
        self.toplevel.destroy()
        self.toplevel = None
        
    def setValues(self):
        print("updating values")
        self.title.set("Weather Forecast")
        self.temperature.set(self.weatherData.temperature)
        self.wind_speed.set(self.weatherData.wind_speed)
        self.wind_direction.set(self.weatherData.wind_direction)
        self.pressure.set(self.weatherData.pressure)
        self.humidity.set(self.weatherData.humidity)
        self.conditions.set(self.weatherData.conditions)
        self.last_updated.set(self.weatherData.last_updated)
        self.heat_index.set(self.weatherData.heat_index)
        self.location.set(self.weatherData.location)
        
    def __init__(self, root):
    
        self.url = None
        self.url = "http://w1.weather.gov/xml/current_obs/KEWR.rss"
        self.root = root
        root.title("Weather Forecast")
        self.toplevel = None
        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E)
        
        #get WeatherData object
        try:
            self.weatherData = wp.WeatherData(self.url)
        except weather_parser.invalidUrl:
            self.weatherData = None
           
        self.title = tk.StringVar()
        self.temperature = tk.StringVar()
        self.wind_speed = tk.StringVar()
        self.wind_direction = tk.StringVar()
        self.last_updated = tk.StringVar()
        self.heat_index = tk.StringVar()
        self.location = tk.StringVar()
        self.pressure = tk.StringVar()
        self.humidity = tk.StringVar()
        self.conditions = tk.StringVar()
        
        self.setValues()
        
        self.button_refresh = tk.Button(self.frame, text="Refresh", command=self.refreshData)
        self.button_change_rss = tk.Button(self.frame, text="Change RSS Feed", command=self.changeRSS)
        
        self.title_label = tk.Label(self.frame, textvariable=self.title)
        self.location_label = tk.Label(self.frame, textvariable=self.location)
        self.wind_speed_label = tk.Label(self.frame, textvariable=self.wind_speed)
        self.wind_direction_label = tk.Label(self.frame, textvariable=self.wind_direction)
        self.heat_index_label = tk.Label(self.frame, textvariable=self.heat_index)
        self.temperature_label = tk.Label(self.frame, textvariable=self.temperature)  
        self.conditions_label = tk.Label(self.frame, textvariable=self.conditions)        
        self.pressure_label = tk.Label(self.frame, textvariable=self.pressure)       
        self.humidity_label = tk.Label(self.frame, textvariable=self.humidity)      
        self.last_updated_label = tk.Label(self.frame, textvariable=self.last_updated)
        
        self.title_label.grid(column=0, row=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.button_refresh.grid(column=0, row=1)
        self.button_change_rss.grid(column=1, row=1)
        self.temperature_label.grid(column=1, row=2)
        self.conditions_label.grid(column=0, row=2)
        self.pressure_label.grid(column=0, row=3)
        self.humidity_label.grid(column=1, row=3)
        self.wind_speed_label.grid(column=0, row=4)
        self.wind_direction_label.grid(column=1, row=4) 
        self.heat_index_label.grid(column=0, row=5)
        self.last_updated_label.grid(column=0, row=6)
        self.location_label.grid(column=1, row=6)
        
        for x in range(7):
            self.frame.grid_rowconfigure(x, weight=1)
        for y in range(2):
            self.frame.grid_columnconfigure(y, weight=1)
    
class ChangeRSSWindow(tk.Toplevel):

    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.rssEntry.get()
        if wp.WeatherData.isValidRSS(rss) is True:
            self.app.getTopLevelRSS(rss)
            self.app.toplevel = None
            self.destroy()
        else:
            print("invalid url")
 
    def __init__(self, master, app):
        tk.Toplevel.__init__(self,master)
        self.app = app
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0)
        tk.Label(self.frame, text="Enter the url of the RSS feed:").grid(column=0, row=0)
        self.rssEntry = tk.Entry(self.frame)
        self.rssEntry.grid(column=0, row=1)
        self.submitRSSButton = tk.Button(self.frame, text="Submit", command=self.pressedSubmit)
        self.submitRSSButton.grid(column=1, row=1)
        

def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    display = WeatherDisplay(root)
    display.weatherData.display()
    root.mainloop()
    
if __name__ == '__main__': main()