import tkinter as tk
from tkinter import ttk
import weather_parser as wp

class WeatherView(tk.Frame):
    '''
    Main window in the MVC of the application.  Displays the parsed information onto the screen
    '''
    def __init__(self, root, weatherObj=None, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E)
        self.toplevel_1 = None
        root.title("Weather Forecast")
        
        self.refresh_button = tk.Button(self, text="Refresh")
        self.change_rss_button = tk.Button(self, text="Change RSS Feed")
        
        #declare each data member as a StringVar
        self.temperature = tk.StringVar()
        self.wind_speed = tk.StringVar()
        self.wind_direction = tk.StringVar()
        self.last_updated = tk.StringVar()
        self.heat_index = tk.StringVar()
        self.location = tk.StringVar()
        self.pressure = tk.StringVar()
        self.humidity = tk.StringVar()
        self.conditions = tk.StringVar()
        
        #if user supplied weather object, set that and update values in the respective StringVars
        if type(weatherObj) is wp.WeatherData:
            self.weatherObj = weatherObj
            self.setValues(weatherObj)
        else:
            self.weatherObj = wp.WeatherData()
            
        #create a label for each data member
        self.title_label = tk.Label(self, text="Weather Forecast")
        self.location_label = tk.Label(self, textvariable=self.location)
        self.wind_speed_label = tk.Label(self, textvariable=self.wind_speed)
        self.wind_direction_label = tk.Label(self, textvariable=self.wind_direction)
        self.heat_index_label = tk.Label(self, textvariable=self.heat_index)
        self.temperature_label = tk.Label(self, textvariable=self.temperature)  
        self.conditions_label = tk.Label(self, textvariable=self.conditions)        
        self.pressure_label = tk.Label(self, textvariable=self.pressure)       
        self.humidity_label = tk.Label(self, textvariable=self.humidity)      
        self.last_updated_label = tk.Label(self, textvariable=self.last_updated)
        
        #set initial placements of the labels
        self.title_label.grid(column=0, row=0, columnspan=2)
        self.refresh_button.grid(column=0, row=1)
        self.change_rss_button.grid(column=1, row=1)
        self.temperature_label.grid(column=1, row=2)
        self.conditions_label.grid(column=0, row=2)
        self.pressure_label.grid(column=0, row=3)
        self.humidity_label.grid(column=1, row=3)
        self.wind_speed_label.grid(column=0, row=4)
        self.wind_direction_label.grid(column=1, row=4) 
        self.heat_index_label.grid(column=0, row=5)
        self.last_updated_label.grid(column=0, row=6)
        self.location_label.grid(column=1, row=6)
        
        #allow labels to resize along with resizing windows
        for x in range(7):
            self.grid_rowconfigure(x, weight=1)
        for y in range(2):
            self.grid_columnconfigure(y, weight=1)
        
    def setValues(self, weatherObj):
        print("updating values")
        self.temperature.set(weatherObj.temperature)
        self.wind_speed.set(weatherObj.wind_speed)
        self.wind_direction.set(weatherObj.wind_direction)
        self.pressure.set(weatherObj.pressure)
        self.humidity.set(weatherObj.humidity)
        self.conditions.set(weatherObj.conditions)
        self.last_updated.set(weatherObj.last_updated)
        self.heat_index.set(weatherObj.heat_index)
        self.location.set(weatherObj.location)
        
        
class ChangeRSSWindow(tk.Toplevel):
 
    def __init__(self, root):
        tk.Toplevel.__init__(self,root)
        self.root = root
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        tk.Label(self.frame, text="Enter the url of the RSS feed:").grid(column=0, row=0)
        self.rssEntry = tk.Entry(self.frame, width=50)
        self.rssEntry.grid(column=0, row=1)
        self.submit_rss_button = tk.Button(self.frame, text="Submit")
        self.submit_rss_button.grid(column=1, row=1)
        
        #allow labels to resize along with resizing windows
        for x in range(2):
            self.grid_rowconfigure(x, weight=1)
        for y in range(2):
            self.grid_columnconfigure(y, weight=1)
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    testObj = wp.WeatherData("http://w1.weather.gov/xml/current_obs/KEWR.rss")
    display = WeatherView(root, testObj).grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E)
       
    #display.weatherData.display()
    root.mainloop()

if __name__ == "__main__": main()