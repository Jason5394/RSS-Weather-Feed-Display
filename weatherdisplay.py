import weather_rss
import tkinter as tk
from tkinter import ttk

class WeatherDisplay:
    '''Application to display weather from an RSS feed.'''
    
    def refreshData(self):
        print("refreshing data from rss")
        self.weatherData = weather_rss.weatherParser(self.url)
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
        self.temp.set(self.weatherData.temp)
        self.desc.set(self.weatherData.desc)
        self.press.set(self.weatherData.press)
        self.hum.set(self.weatherData.hum)
        self.cond.set(self.weatherData.cond)
        
    def __init__(self, url, root):
        counter = 0
        self.root = root
        root.title("Weather Forecast")
        self.url = url
        self.toplevel = None
        self.frame = tk.Frame(self.root)
        self.frame.grid(column=0, row=0)
        
        #get WeatherData object
        self.weatherData = weather_rss.weatherParser(url)
        self.title = tk.StringVar()
        self.temp = tk.StringVar()
        self.desc = tk.StringVar()
        self.press = tk.StringVar()
        self.hum = tk.StringVar()
        self.cond = tk.StringVar()
        
        self.setValues()
        
        self.button_refresh = tk.Button(self.frame, text="Refresh", command=self.refreshData)
        self.button_change_rss = tk.Button(self.frame, text="Change RSS Feed", command=self.changeRSS)
        
        self.button_refresh.grid(column=0, row=2)
        self.button_change_rss.grid(column=1, row=2)
                
        self.title_label = tk.Label(self.frame, textvariable=self.title)
        self.temp_label = tk.Label(self.frame, textvariable=self.temp)  
        self.cond_label = tk.Label(self.frame, textvariable=self.cond)        
        self.press_label = tk.Label(self.frame, textvariable=self.press)       
        self.hum_label = tk.Label(self.frame, textvariable=self.hum)      
        self.desc_label = tk.Label(self.frame, textvariable=self.desc)
        
        self.desc_label.grid(column=0, row=5)
        self.title_label.grid(column=0, row=1)
        self.temp_label.grid(column=1, row=3)
        self.cond_label.grid(column=0, row=3)
        self.press_label.grid(column=0, row=4)
        self.hum_label.grid(column=1, row=4)
    
class ChangeRSSWindow(tk.Toplevel):

    def pressedSubmit(self):
        #check validity of URL here
        #if okay, exit out of window and save new url otherwise show warning message
        rss = self.rssEntry.get()
        if weather_rss.isValidRSS(rss) == 1:
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
    display = WeatherDisplay("http://w1.weather.gov/xml/current_obs/KEWR.rss", root)
    display.weatherData.display()
    root.mainloop()
    
if __name__ == '__main__': main()