""" Get local weather data from the DarkSky API """

import requests
from os import path
from scripts.py.application import logger

appPath = path.dirname(path.abspath(__file__))

name = 'Forecast-Weather'
log = logger.setup_logger(name)

iconDir = path.abspath(path.dirname(__file__) + '/media/icons/weather_conditions/static')
print(iconDir)
mediaDir = path.abspath(appPath + '/media')
imagesDir = path.abspath(mediaDir + '/images')

darkSkyURL = 'https://api.darksky.net/forecast/'


def conn_image(status):
    global imagesDir, mediaDir
    if status:
        return imagesDir + '/light_on.png'
    else:
        return imagesDir + '/light_off.png'


def get_compass(num):
    val = int((num / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def check_key(key):
    global mediaDir
    log.debug('Checking provided key')
    test_url = darkSkyURL + key + '/37.8267,-122.4233'
    res = requests.get(test_url)
    if res.status_code == 200:
        log.info('Valid key!')
        return True
    else:
        log.warning('Invalid key!')
        log.debug('Popping popup to advise user of this')
        return False


def getWeather(lat, lon, api_key):
    sep = ','
    cords = str(str(lat) + sep + str(lon))
    apiURL = 'https://api.darksky.net/forecast/%s' % api_key + '/' + cords
    res = requests.get(apiURL)
    if res.status_code == 200:
        print(res.json()['currently'])
        return res.json()['currently']
    else:
        log.warn('Invalid status code returned from API request')


def getIcon(icon):
    global iconDir

    if icon == 'clear-night':
        return str(iconDir + '/night.png')

    if icon == 'clear-day':
        return str(iconDir + '/day.png')
