import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
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
        self.toplevel_2 = None
        root.title("Weather Forecast")
        root.geometry("450x280")
        root.resizable(0,0)
        self.refresh_button = tk.Button(self, text="Update")
        self.change_rss_button = tk.Button(self, text="Change RSS feed")
        self.show_src_button = tk.Button(self, text="Show source")
        
        self.conditions_img = None
        
        #declare each data member as a StringVar
        self.temperature = tk.StringVar()
        self.wind = tk.StringVar()
        #self.wind_direction = tk.StringVar()
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
        self.title_label = tk.Label(self, text="Weather Forecast", font="bold")
        self.location_label = tk.Label(self, textvariable=self.location)
        self.wind_label = tk.Label(self, textvariable=self.wind)
        self.heat_index_label = tk.Label(self, textvariable=self.heat_index)
        self.temperature_label = tk.Label(self, textvariable=self.temperature, font="Calibri, 24")  
        self.conditions_label = tk.Label(self, textvariable=self.conditions, font="Calibri, 20")        
        self.pressure_label = tk.Label(self, textvariable=self.pressure)       
        self.humidity_label = tk.Label(self, textvariable=self.humidity)      
        self.last_updated_label = tk.Label(self, textvariable=self.last_updated)
        self.conditions_img_label = tk.Label(self, image=self.conditions_img)
        #static labels that don't change
        self.location_static_label = tk.Label(self, text="Location: ")
        self.heat_static_label = tk.Label(self, text="Heat index: ")
        self.pressure_static_label = tk.Label(self, text="Pressure: ")
        self.humidity_static_label = tk.Label(self, text="Humidity: ")
        self.updated_static_label = tk.Label(self, text="Last Updated: ")
        self.wind_static_label = tk.Label(self, text="Wind conditions: ")
        
        #set grid placements of the labels
        self.title_label.grid(column=1, row=0)
        self.refresh_button.grid(column=0, row=1, sticky=tk.E)
        self.change_rss_button.grid(column=1, row=1)
        self.show_src_button.grid(column=2, row=1, sticky=tk.W)
        self.conditions_label.grid(column=0, row=2, sticky=tk.E)
        self.conditions_img_label.grid(column=1, row=2)
        self.temperature_label.grid(column=2, row=2, sticky=tk.W)
        self.pressure_static_label.grid(column=0, row=3, sticky=tk.E)
        self.pressure_label.grid(column=1, row=3, columnspan=2, sticky=tk.W)
        self.humidity_static_label.grid(column=0, row=4, sticky=tk.E)
        self.humidity_label.grid(column=1, row=4, columnspan=2, sticky=tk.W)
        self.wind_static_label.grid(column=0, row=5, sticky=tk.E)
        self.wind_label.grid(column=1, row=5, columnspan=2, sticky=tk.W)
        self.heat_static_label.grid(column=0, row=6, sticky=tk.E)
        self.heat_index_label.grid(column=1, row=6, columnspan=2, sticky=tk.W)
        self.updated_static_label.grid(column=0, row=7, sticky=tk.E)
        self.last_updated_label.grid(column=1, row=7, columnspan=2, sticky=tk.W)
        self.location_static_label.grid(column=0, row=8, sticky=tk.E)
        self.location_label.grid(column=1, row=8, columnspan=2, sticky=tk.W)
        
        #allow labels to resize along with resizing windows
        for x in range(9):
            self.grid_rowconfigure(x, weight=1)
        for y in range(3):
            self.grid_columnconfigure(y, weight=1)
        
    def setValues(self, weatherObj):
        print("updating values")
        degree_sign= u'\N{DEGREE SIGN}'
        self.temperature.set(wp.toString(weatherObj.temperature)+degree_sign)
        self.pressure.set(wp.toString(weatherObj.pressure) + " mb")
        self.humidity.set(wp.toString(weatherObj.humidity) + "%")
        self.conditions.set(wp.toString(weatherObj.conditions))
        self.last_updated.set(wp.toString(weatherObj.last_updated))
        self.heat_index.set(wp.toString(weatherObj.heat_index))
        self.location.set(wp.toString(weatherObj.location))
        
        wind_string = ""
        wind_exists = False
        if weatherObj.wind_direction is not None:
            wind_string += weatherObj.wind_direction + " "
            wind_exists = True
        if weatherObj.wind_speed is not None:
            wind_string += weatherObj.wind_speed + " MPH"
            wind_exists = True
        if wind_exists is True:
            self.wind.set(wind_string)
        else:
            self.wind.set("n/a")
            
        
        if weatherObj.img_url is not None:
            r = requests.get(weatherObj.img_url)
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(r.content)))
            self.conditions_img_label.configure(image=img)
            self.conditions_img_label.image = img
            
            
class ShowSourceWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.resizable(0,0)
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        tk.Label(self.frame, text="RSS Source", font="bold").grid(column=0, row=0)
        self.rss_src = tk.StringVar()
        rss_src_label = tk.Label(self.frame, textvariable=self.rss_src)
        rss_src_label.grid(column=0, row=1)
        
    def setSrc(self, src_string):
        self.rss_src.set(src_string)
 
class ChangeRSSWindow(tk.Toplevel):
 
    def __init__(self, root):
        tk.Toplevel.__init__(self,root)
        self.root = root
        self.resizable(0,0)
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        tk.Label(self.frame, text="Enter the url of the RSS feed:").grid(column=0, row=0)
        self.rss_entry = tk.Entry(self.frame, width=50)
        self.rss_entry.grid(column=0, row=1)
        self.submit_rss_button = tk.Button(self.frame, text="Submit")
        self.submit_rss_button.grid(column=1, row=1)
        
        #allow labels to resize along with resizing windows
        # for x in range(2):
            # self.grid_rowconfigure(x, weight=1)
        # for y in range(2):
            # self.grid_columnconfigure(y, weight=1)
            
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    testObj = wp.WeatherData("http://w1.weather.gov/xml/current_obs/KEWR.rss")
    display = WeatherView(root, testObj).grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E)
       
    #display.weatherData.display()
    root.mainloop()

if __name__ == "__main__": main()