""" Get local weather data from the DarkSky API """

import requests
from os import path
from scripts.py.application import logger

name = 'Forecast-Weather'
log = logger.setup_logger(name)

iconDir = path.abspath(path.dirname(__file__) + '/media/icons/weather_conditions/static')

darkSkyURL = 'https://api.darksky.net/forecast/'


def check_key(key):
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


def getWeather(lat, lng, api_key):
    apiURL = 'https://api.darksky.net/forecast/%s' % api_key + '/' + lat + ',' + lng
    res = requests.get(apiURL)
    if res.status_code == 200:
        return res.json()['currently']
    else:
        log.warn('Invalid status code returned from API request')
        print(res.json())


def getIcon(icon):
    global iconDir

    if icon == 'clear-night':
        return str(iconDir + '/night.png')
