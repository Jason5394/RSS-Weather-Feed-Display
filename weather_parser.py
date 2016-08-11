import feedparser
import re

class parseError(Exception):
    pass

class WeatherData:
    '''Class to hold pertinent weather data
        Also contains methods to parse RSS feeds from w1.weather.gov'''
    
    
    def __init__(self, url):
        self.url = url
        
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
    
    def weatherParser(self):
        # d = feedparser.parse(url)
        # title = d.entries[0]['title']
        # desc = d.entries[0]['description']
        # weathercond, remainder = re.split(' and ', title)
        # temp, location = re.split(' F at ', remainder)
        # temp = float(temp)
        # link, remainder2 = re.split('<br />', desc)
        # description, remainder2 = re.split(' The pressure is ', remainder2)
        # pressure, humidity = re.split(' mb and the humidity is ', remainder2)
        # pressure = float(pressure)
        # humidity = int(humidity[0:2])
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
            pass
            raise parseError("An error occured in weatherParser().")
    
    
        #return WeatherData(weathercond, temp, description, pressure, humidity)
    
    def display(self):
        print("Conditions\t", self.conditions)
        print("Temperature\t", self.temperature)
        print("Location\t", self.location)
        print("Wind Direction\t", self.wind_direction)
        print("Wind Speed\t", self.wind_speed)
        print("Pressure\t", self.pressure)
        print("Humidity\t", self.humidity)
        print("Heat Index\t", self.heat_index)
        print("Last Updated\t", self.last_updated)
  
def isValidRSS(url):
    return 1
        
def weatherParser(url):
    d = feedparser.parse(url)
    title = d.entries[0]['title']
    desc = d.entries[0]['description']
    weathercond, remainder = re.split(' and ', title)
    temp, location = re.split(' F at ', remainder)
    temp = float(temp)
    link, remainder2 = re.split('<br />', desc)
    description, remainder2 = re.split(' The pressure is ', remainder2)
    pressure, humidity = re.split(' mb and the humidity is ', remainder2)
    pressure = float(pressure)
    humidity = int(humidity[0:2])
    
    return WeatherData(weathercond, temp, description, pressure, humidity)
    

def main():
    testObj = WeatherData("http://w1.weather.gov/xml/current_obs/NSTU.rss")
    #weatherData = weatherParser("http://w1.weather.gov/xml/current_obs/KEWR.rss")
    #testObj.weatherParser()
	
if __name__ == '__main__': main()