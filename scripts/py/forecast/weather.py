""" Get local weather data from the DarkSky API """

import requests
from os import path
from scripts.py.application import logger
import random
import json

appPath = path.dirname(path.abspath(__file__))

name = 'Forecast-Weather'
log = logger.setup_logger(name)

iconDir = path.abspath(path.dirname(__file__) + '/media/icons/weather_conditions/static')
log.debug('Found weather icon dir: %s' % iconDir)
mediaDir = path.abspath(appPath + '/media')
imagesDir = path.abspath(mediaDir + '/images')

darkSkyURL = 'https://api.darksky.net/forecast/'
log.info('Weather data provided by Forecast.io')

def conn_image(status):
    global imagesDir, mediaDir
    if status:
        return imagesDir + '/light_on.png'
    else:
        return imagesDir + '/light_off.png'


def get_compass(num):
    val = int((int(num) / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def check_key(key):
    global mediaDir, log
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
    global log
    sep = ','
    cords = str(str(lat) + sep + str(lon))
    apiURL = 'https://api.darksky.net/forecast/%s' % api_key + '/' + cords
    log.debug('Fetching data from https://api.darksky.net/forecast....')
    res = requests.get(apiURL)
    log.debug('Request status: %i' % res.status_code)
    if res.status_code == 200:

        data = res.json()['currently']
        log.debug('Stringifying data...')
        log.debug('Was: %s' % data)
        data = json.loads(json.dumps(data), parse_int=str)
        log.debug('Stringified version: %s' % data)

        return data
    else:
        log.warn('Invalid status code returned from API request')


def getIcon(icon):
    global iconDir, log
    log.debug('Fetching new condition icon')

    variation_list = ['1.png', '2.png', '3.png']

    if icon == 'clear-night':
        icon = str(iconDir + '/night.png')

    if icon == 'clear-day':
        icon = str(iconDir + '/day.png')

    if icon == 'partly-cloudy-day':
        pick = random.sample(variation_list, 1)
        pick = ''.join(pick)
        icon = str(iconDir + '/cloudy-day-' + pick)

    if icon == 'partly-cloudy-night':
        pick = random.sample(variation_list, 1)
        pick = ''.join(pick)
        icon = str(iconDir + '/cloudy-night-' + pick)

    log.debug('Giving GUI this icon: %s' % icon)
    return icon
