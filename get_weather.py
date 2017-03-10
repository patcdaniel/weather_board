from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def get_mlml_weather():

    '''
    Get latest wind speed, wind dir and air temp from MLML pubdata site
    returns:
        - windSpeed = Meters per second
        - windDir = Wind direction in degrees from North
        - airTemp = Air Temperture in degrees F
    '''


    url = "http://pubdata.mlml.calstate.edu/weather/recent.html"
    content = urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    out = [tr.find('td').text for tr in soup.findAll('tr')]
    data = out[1]
    data = data.split('\n')
    data = [l for l in data if l != '']
    data = [l.strip('> ') for l in data]
    for i,l in enumerate(data):
        if l.lower().find('wind speed') != -1:
            windSpeed = float((re.search('Wind Speed:(\d+\.\d+) m/s.+',l).group(1)))
        elif l.lower().find('wind direction') != -1:
            windDir = int((re.search('Wind Direction:(\d+).+',l).group(1)))
        elif l.lower().find('air temperature') != -1:
            airTemp = float((re.search('Air Temperature:(\d+\.\d+).+',l).group(1)))
    return windSpeed,windDir,airTemp
      
      
