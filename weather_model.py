import weather_parser as wp
from pubsub import pub

class WeatherModel: 
    '''
    Model in the MVC of the application.
    '''
    def __init__(self):
        self.weatherObj = None
        self.url = None
        
    def setWeather(self, url):
        self.url = url
        self.weatherObj = wp.WeatherData(self.url)
        pub.sendMessage("valuesChanged", url=str(self.url))

    def getUrl(self):   
        return self.url
        
    def getWeatherObj(self):
        return self.weatherObj