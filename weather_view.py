import requests
import io
import weather_parser as wp
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import weather_menu as wm

class WeatherView(ttk.Frame):
    '''
    Main window in the MVC of the application.  Displays the parsed information onto the screen
    '''
    def __init__(self, root, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.grid(column=0, row=0, sticky="nsew")
        self.toplevels = {"changeRSS": None, "showFeed": None}
        self.conditions_img = None
        root.title("Weather Forecast")
        root.resizable(0,0)
        
        width = 450
        height = 280
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (width/2)
        y = (hs/2) - (height/2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        
        #create subframes inside main frame
        self.topframe = ttk.Frame(self, height=40)
        self.midframe = ttk.Frame(self, height=100)
        self.botframe = ttk.Frame(self, height=140)
        self.topframe.grid(column=0, row=0)
        self.midframe.grid(column=0, row=1, sticky="ns")
        self.botframe.grid(column=0, row=2, sticky="nsew")
        
        #declare each data member as a StringVar
        self.temperature = tk.StringVar()
        self.wind = tk.StringVar()
        self.last_updated = tk.StringVar()
        self.heat_index = tk.StringVar()
        self.location = tk.StringVar()
        self.pressure = tk.StringVar()
        self.humidity = tk.StringVar()
        self.conditions = tk.StringVar()
         
        #creating buttons 
        self.refresh_button = ttk.Button(self.topframe, text="Update", width=12)
        self.change_rss_button = ttk.Button(self.topframe, text="Change feed", width=12)
        self.show_src_button = ttk.Button(self.topframe, text="Show source", width=12)    
            
        #create a label for each data member
        self.title_label = ttk.Label(self.topframe, text="Weather Forecast", font="bold")
        
        self.temperature_label = ttk.Label(self.midframe, textvariable=self.temperature,
                                            padding=5, font="Calibri, 24") 
        self.conditions_img_label = ttk.Label(self.midframe, image=self.conditions_img)               
        self.conditions_label = ttk.Label(self.midframe, textvariable=self.conditions,
                                            padding=5, font="Calibri, 18")    
        
        self.pressure_label = ttk.Label(self.botframe, textvariable=self.pressure)     
        self.humidity_label = ttk.Label(self.botframe, textvariable=self.humidity)      
        self.wind_label = ttk.Label(self.botframe, textvariable=self.wind)
        self.heat_index_label = ttk.Label(self.botframe, textvariable=self.heat_index) 
        self.last_updated_label = ttk.Label(self.botframe, textvariable=self.last_updated)
        self.location_label = ttk.Label(self.botframe, textvariable=self.location)
        #static labels that don't change
        self.pressure_static_label = ttk.Label(self.botframe, text="Pressure: ")
        self.humidity_static_label = ttk.Label(self.botframe, text="Humidity: ")
        self.wind_static_label = ttk.Label(self.botframe, text="Wind conditions: ")
        self.heat_static_label = ttk.Label(self.botframe, text="Heat index: ") 
        self.location_static_label = ttk.Label(self.botframe, text="Location: ")
        self.updated_static_label = ttk.Label(self.botframe, text="Last updated: ")
          
        #set grid placements of the widgets
        
        #top frame widgets
        self.title_label.grid(column=0, row=0, columnspan=3)
        self.refresh_button.grid(column=0, row=1)
        self.change_rss_button.grid(column=1, row=1)
        self.show_src_button.grid(column=2, row=1)
        #mid frame widgets
        self.conditions_label.grid(column=0, row=0)
        self.conditions_img_label.grid(column=1, row=0)
        self.temperature_label.grid(column=2, row=0)
        #bot frame widgets
        self.pressure_static_label.grid(column=0, row=0, sticky="e", padx=4)
        self.pressure_label.grid(column=1, row=0, sticky="w")
        self.humidity_static_label.grid(column=0, row=1, sticky="e", padx=4)
        self.humidity_label.grid(column=1, row=1, sticky="w")
        self.wind_static_label.grid(column=0, row=2, sticky="e", padx=4)
        self.wind_label.grid(column=1, row=2, sticky="w")
        self.heat_static_label.grid(column=0, row=3, sticky="e", padx=4)
        self.heat_index_label.grid(column=1, row=3, sticky="w")
        self.updated_static_label.grid(column=0, row=4, sticky="e", padx=4)
        self.last_updated_label.grid(column=1, row=4, sticky="w")
        self.location_static_label.grid(column=0, row=5, sticky="e", padx=4)
        self.location_label.grid(column=1, row=5, sticky="w")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.topframe.grid_columnconfigure(0, weight=1)
        self.topframe.grid_columnconfigure(1, weight=1)
        self.topframe.grid_columnconfigure(2, weight=1)
        self.topframe.grid_rowconfigure(0, weight=1)
        self.midframe.grid_columnconfigure(0, weight=0)
        self.midframe.grid_columnconfigure(1, weight=1)
        self.midframe.grid_columnconfigure(2, weight=0)
        self.midframe.grid_rowconfigure(0, weight=1)
        self.botframe.grid_columnconfigure(0, weight=1)
        self.botframe.grid_columnconfigure(1, weight=3)
        for row in range(6):
            self.botframe.grid_rowconfigure(row, weight=1)
            
    def setValues(self, weatherdict):
        print("updating values")
        self.weatherdict = weatherdict
        degree_sign= u'\N{DEGREE SIGN}'
        
        if weatherdict["temperature"]:
            self.temperature.set(weatherdict["temperature"] + degree_sign)
        if weatherdict["conditions"]:
            self.conditions.set(weatherdict["conditions"])
        self.pressure.set(wp.toString(weatherdict["pressure"]) + " mb")
        self.humidity.set(wp.toString(weatherdict["humidity"]) + "%")     
        self.last_updated.set(wp.toString(weatherdict["last_updated"]))
        self.heat_index.set(wp.toString(weatherdict["heat_index"]))
        self.location.set(wp.toString(weatherdict["location"]))
        
        wind_string = ""
        wind_exists = False
        if weatherdict["wind_direction"] is not None:
            wind_string += weatherdict["wind_direction"] + " "
            wind_exists = True
        if weatherdict["wind_speed"] is not None:
            wind_string += weatherdict["wind_speed"] + " MPH"
            wind_exists = True
        if wind_exists is True:
            self.wind.set(wind_string)
        else:
            self.wind.set("n/a")
                  
        if weatherdict["img_url"] is not None:
            r = requests.get(weatherdict["img_url"])
            with Image.open(io.BytesIO(r.content)) as fp:
                img = ImageTk.PhotoImage(fp)
                self.conditions_img_label.configure(image=img)
                self.conditions_img_label.image = img      
        else:
            self.conditions_img_label.configure(image=None)
            self.conditions_img_label.image = None
 
 
class FormTopLevel(tk.Toplevel):

    def __init__(self, root, title=None, resizable=False, **kwargs):

        tk.Toplevel.__init__(self, root, **kwargs)
        #self.transient(root)
        self.root = root
        if title:
            self.title(title) 
        if not resizable:
            self.resizable(0,0)
        self.focus_set()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.removeTopLevel)
        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))
                                  
        self.frame = ttk.Frame(self)   
        self.frame.grid(column=0, row=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def removeTopLevel(self, event=None):
        self.root.focus_set()
        self.destroy()
        self = None
        
            
class ShowSourceWindow(FormTopLevel):
    def __init__(self, root, src="", **kwargs):
        FormTopLevel.__init__(self, root, **kwargs)
        
        self.rss_src = src
        ttk.Label(self.frame, text="RSS Source", font="bold").grid(column=0, row=0)
        rss_src_label = ttk.Label(self.frame, text=self.rss_src)
        rss_src_label.grid(column=0, row=1)
  
  
class ChangeRSSWindow(FormTopLevel):
 
    def __init__(self, root, **kwargs):
        FormTopLevel.__init__(self,root, **kwargs)
        
        ttk.Label(self.frame, text="Enter the url of the RSS feed:").grid(column=0, row=0)
        self.rss_entry = ttk.Entry(self.frame, width=50)
        self.rss_entry.grid(column=0, row=1)
        self.submit_rss_button = ttk.Button(self.frame, text="Submit")
        self.submit_rss_button.grid(column=1, row=1)
      
        
def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__": main()