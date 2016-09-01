import weather_parser as wp
import pickle
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
        self.__loadFromFile()
        print("saved_urls: ", self.saved_urls)
        print("saved_names: ", self.saved_names)
        if self.url is not None:
            print("printing url: ", self.url)
        else:
            print("url was not found")
        
    def __saveToFile(self):
        with open("saved_feeds.pickle", "wb") as handle:
            #pack url list, name list, and current url to dict and save dict to file
            saved_dict = {"savedNames" : self.saved_names, "savedUrls" : self.saved_urls, "recentUrl" : self.url}
            pickle.dump(saved_dict, handle)
            
    def __loadFromFile(self):
        try:
            with open("saved_feeds.pickle", "rb") as handle:
                try:
                    dict = pickle.load(handle)
                    print("dict:",dict)
                    self.saved_urls = dict["savedUrls"]
                    self.saved_names = dict["savedNames"]
                    if wp.WeatherData.isValidRSS(dict["recentUrl"]): 
                        self.setWeather(dict["recentUrl"])
                    else:
                        self.url = None
                        self.weatherObj = None
                        self.weather_dict = None
                except EOFError:
                    print("No data from file")
                    self.__clear()
                except pickle.UnpicklingError:
                    print("Problem unpickling saved data.  Program will wipe corrupt data.")
                    #TODO: implement wiping of persistent data on file
                    self.__clear()  #clears local data
                    #TODO: Send message to notify user of data corruption.
        except FileNotFoundError:
            print("FileNotFoundError caught")
            self.__clear()
            return
        
    def __clear(self):
        '''sets all member variables to be None or empty'''
        self.weatherObj = None
        self.weather_dict = None
        self.url = None
        self.saved_urls = []
        self.saved_names = []
        
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
            self.__saveToFile()
            pub.sendMessage("validSave")
            
    def getUrl(self):   
        return self.url
        
    def getWeatherObj(self):
        return self.weatherObj
        
    def getWeatherDict(self):
        return self.weather_dict
        
    def getSavedUrls(self):
        return self.saved_urls
        
    def getSavedNames(self):
        return self.saved_names
        
        
        
        
        
        
        