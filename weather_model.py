import weather_parser as wp
from pubsub import pub

class WeatherModel: 
    '''
    Model in the MVC of the application.
    '''
    def __init__(self):
        self.weatherObj = None
        self.weather_dict = None
        self.url = None   
        self.saved_urls = []
        self.saved_names = []
        self.saved_urls.append("http://w1.weather.gov/xml/current_obs/NSTU.rss")
        self.saved_names.append("test")
        
    def setWeather(self, url):
        self.url = url
        self.weatherObj = wp.WeatherData(self.url)
        self.weather_dict = self.weatherObj.__dict__ #dictionary that contains all weatherObj attributes
        pub.sendMessage("valuesChanged", weather_dict=self.weather_dict)

    def addSavedUrl(self, saved_url, saved_name):
        print("saved_url:", saved_url, "saved_name:", saved_name)
        if saved_name in self.saved_names:
            print("sending invalidurl message:")
            pub.sendMessage("invalidSave", message="RSS feed name already exists.")
        elif saved_url in self.saved_urls:
            pub.sendMessage("invalidSave", message="RSS url already exists.")
        else:
            print("validsave")
            self.saved_urls.insert(0, saved_url)
            self.saved_names.insert(0, saved_name)
            pub.sendMessage("validSave")
        
    # def addSavedUrl(self, saved_url, saved_name):
        # print("saved_url:", saved_url, "saved_name:", saved_name)
        # if saved_name in self.saved_names:
            # print("sending invalidurl message:")
            # pub.sendMessage("savingUrl", message="RSS feed name already exists.")
        # elif saved_url in self.saved_urls:
            # pub.sendMessage("savingUrl", message="RSS url already exists.")
        # else:
            # print("validsave")
            # self.saved_urls.insert(0, saved_url)
            # self.saved_names.insert(0, saved_name)
            # pub.sendMessage("savingUrl", message=None)
            
    def getUrl(self):   
        return self.url
        
    def getWeatherObj(self):
        return self.weatherObj
        
    def getWeatherDict(self):
        return self.weather_dict
        
        
        
        
        
        
        