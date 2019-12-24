""" Get realtime access to weather through the DarkSky API as well as data from various supported environment sensors """

import PySimpleGUI as sg
import os.path as path
import sys
sys.path.append(path.abspath('.'))
from scripts.py.application.logger import setup_logger
from scripts.py.forecast.IPtoGP import getByIP
from scripts.py.forecast.weather import check_key
from scripts.py.forecast.weather import getWeather
from scripts.py.forecast.weather import getIcon

name = 'Forecast'

log = setup_logger(name)
log.info('The logger is awake')

from scripts.py.application import itsmConfig as config

log.debug('Determining where in the filesystem I am')


appPath = path.dirname(path.abspath(__file__))
log.debug(' Found path: %s' % appPath)

confPath = path.abspath(appPath + '/forecast/conf')

existingConfFilepath = path.abspath(confPath + '/forecast_conf.json')

if path.exists(confPath + '/forecast_conf.json'):
    log.info('Found %s' % confPath + '/forecast_conf.json')
    confFile = path.abspath(confPath + '/forecast_conf.json')
else:
    confFile = path.abspath(confPath + '/example_forecast_conf.json')

settings = config.readConf(confFile)['applets']['forecast']['settings']

mediaDir = path.abspath(appPath + '/media')
imagesDir = path.abspath(mediaDir + '/images')

cords = False
address = False

if not settings['address']['lat']:
    log.warn('Unable to find location info in settings. Looking for general location via IP address...')
    log.debug('Calling IPtoGP')
    findAddress = getByIP()
    setAddress = settings['address']
    location = {}
    for key in (findAddress.viewkeys() | setAddress.keys()):
        if key in settings: location.setdefault(key, []).append(settings[key])
        if key in findAddress: location.setdefault(key, []).append(findAddress[key])

else:
    location = settings['address']

region = location['region']
city = location['city']
zipcode = location['zip']
lat = location['lat']
lon = location['lon']

log.debug('Found location information %s' % location)

sg.change_look_and_feel(settings['preferences']['theme'])

log.debug('Looking for darksky API key')
if settings['api']['darksky']['key']:
    log.debug('Found key')
else:
    log.warning('Did not find key!')
    log.debug('Popping up window to ask user for API key')
    key = sg.PopupGetText('Could not find DarkSky API Key. Please enter it below!',)
    log.debug('User entered %s' % key)
    if key is None:
        log.fatal('User did not provide a key and closed the window')
        exit(1)
    else:
        log.info(key)
        settings['api']['darksky']['key'] = key


apiKey = settings['api']['darksky']['key']

if check_key(apiKey):
    log.debug('ConnLight On')
    connLight = True
else:
    log.debug('ConnLight Off')
    connLight = False

appMenu = [['Settings', ['Location']]]

if connLight:
    lightImage = imagesDir + '/light_on.png'
else:
    lightImage = imagesDir + '/light_off.png'
    sg.PopupError('Invalid key!')

weather = getWeather(lat, lon, apiKey)

layout = [
    [sg.Menu(appMenu)],
    [sg.Text('adaWeather', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Frame(layout=[
        [sg.Text('Conditions', justification='left'), sg.Image(getIcon(weather['icon'])),
         sg.InputText(weather['summary'], key='_WSUMMARY_')],
        [sg.Text('Temp', justification='left'), sg.InputText(weather['temperature'], key='temp')]],
        title='Current Weather', relief=sg.RELIEF_SUNKEN, tooltip='Put your GPS cords here')],
    [sg.Button('OK')]
]


mainWin = sg.Window('adaForecast', layout)
prefWinActive = False
localeWinActive = False

while True:
    event, values = mainWin.Read(timeout=100)
    if event is None:
        log.info('User exited the app')
        mainWin.Close()
        exit()

    if not localeWinActive and event == 'Location':
        localeWinActive = True
        log.debug('User entered the location window')

        if settings['address']['lat']:
            guiLat = settings['address']['lat']
            guiLng = settings['address']['lon']

        else:
            guiLat = ''
            guiLng = ''

        localeWinLayout = [
            [sg.Text('Location Information', size=(30, 1), justification='center', font=("Helvetica", 25),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Frame(layout=[
                [sg.Text('Latitude', justification='left'), sg.InputText(guiLat, key='_LAT_')],
                [sg.Text('Longitude', justification='left'), sg.InputText(guiLng, key='_LNG_')]], title='Coordinates',
                relief=sg.RELIEF_SUNKEN, tooltip='Put your GPS cords here')],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]

        localeWin = sg.Window('adaForecast-Location Settings', localeWinLayout)

    if localeWinActive:
        localeEvent, localeVal = localeWin.Read(timeout=100)
        if localeEvent is None or localeEvent == 'Cancel':
            localeWinActive = False
            localeWin.Close()

mainWin.close()
