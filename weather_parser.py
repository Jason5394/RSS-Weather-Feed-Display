import feedparser
import re

class parseError(Exception):
    pass
    
class invalidUrl(Exception):
    pass

class WeatherData:
    '''
    Class to hold pertinent weather data
    Also contains methods to parse RSS feeds from w1.weather.gov
    Note:  As of this time, only RSS feeds from the above mentioned url will work with this
    parser.
    '''
    
    dummyRSS = "w1.weather.gov/xml/current_obs/TEST.rss"
    
    def __init__(self, url):
        '''
        Constructor for WeatherData class.  Checks whether the input url is a valid
        RSS feed from w1.weather.gov.  Initializes each weather data's variable to None, and 
        then attempts to parse values.
        '''
        self.url = url
        
        if not self.isValidRSS():
            raise invalidUrl("The url given in the constructor parameter is invalid.")
           
        
        self.conditions = None
        self.temperature = None
        self.location = None
        self.wind_direction = None
        self.wind_speed = None
        self.pressure = None
        self.humidity = None
        self.heat_index = None
        self.last_updated = None
        
        self.weatherParser()
    
    def isValidRSS(self):
        '''
        Determines if a given url is a valid RSS feed of w1.weather.gov.  Url must 
        contain the string "w1.weather.gov/xml/current_obs/", and must obtain at least
        one item entry for it to be valid.
        '''
        if self.url is not None and re.search("w1.weather.gov/xml/current_obs/", self.url):
            d = feedparser.parse(self.url)
            if len(d.entries) > 0:
                return True
        return False
    
    def weatherParser(self):
        '''
        Parses weather data, and places it into the instance variables.  If the value was not correctly
        parsed, the instance variable stays as None.
        '''
 
        try:
            d = feedparser.parse(self.url)
            rss_title = d.entries[0]['title']
            rss_description = d.entries[0]['description']
            
            #parsing from title tag, variables MUST be filled
            title_match = re.match(r"([\w\s]+) and ([\d]+) F at ([\w\s|,]+)", rss_title)
            self.conditions = title_match.group(1)
            self.temperature = title_match.group(2)
            self.location = title_match.group(3)
           
            #parsing from description tag, variables may or may not be filled
            wind_match = re.search("Winds are (\w+) at (\d+(.)?\d+) MPH", rss_description)
            if wind_match:
                self.wind_direction = wind_match.group(1)
                self.wind_speed = wind_match.group(2)
           
            pressure_match = re.search("pressure is (\d+(.)?\d+) mb", rss_description)
            if pressure_match:
                self.pressure = pressure_match.group(1)
            
            humidity_match = re.search("humidity is (\d+(.)?\d+)%", rss_description)
            if humidity_match:
                self.humidity = humidity_match.group(1)
                
            heat_match = re.search("heat index is (\d+(.)?\d+)", rss_description)
            if heat_match:
                self.heat_index = heat_match.group(1)
                
            last_updated_match = re.search("Last Updated on ([\w\s,:]+)", rss_description)
            if last_updated_match:
                self.last_updated = last_updated_match.group(1)
            
            self.display()
                  
        except Exception:
            raise parseError("An error occured in weatherParser().")

    def display(self):
        '''
        Displays parsed weather data
        '''
        print("Conditions\t", self.conditions)
        print("Temperature\t", self.temperature)
        print("Location\t", self.location)
        print("Wind Direction\t", self.wind_direction)
        print("Wind Speed\t", self.wind_speed)
        print("Pressure\t", self.pressure)
        print("Humidity\t", self.humidity)
        print("Heat Index\t", self.heat_index)
        print("Last Updated\t", self.last_updated)
  
  
def main():
    testObj = WeatherData("http://w1.weather.gov/xml/current_obs/KEWR.rss")
    #weatherData = weatherParser("http://w1.weather.gov/xml/current_obs/KEWR.rss")
    #testObj.weatherParser()
	
if __name__ == '__main__': main()