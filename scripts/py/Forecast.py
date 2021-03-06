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
from scripts.py.forecast.weather import get_compass
from scripts.py.forecast.weather import conn_image

name = 'Forecast'

log = setup_logger(name)
log.info('The logger is awake')

from scripts.py.application import conf

log.debug('Determining where in the filesystem I am')
new_key = False

appPath = path.dirname(path.abspath(__file__))
log.debug(' Found path: %s' % appPath)

confPath = path.abspath(appPath + '/forecast/conf')

existingConfFilepath = path.abspath(confPath + '/forecast_conf.json')

if path.exists(confPath + '/forecast_conf.json'):
    log.info('Found %s' % confPath + '/forecast_conf.json')
    confFile = path.abspath(confPath + '/forecast_conf.json')
else:
    confFile = path.abspath(confPath + '/example_forecast_conf.json')

settings = conf.readConf(confFile)

location = settings['applets']['forecast']['settings']['address']
print(location)
print(settings)

mediaDir = path.abspath(appPath + '/media')

cords = False

if not location['lat']:
    log.warning('Unable to find location info in settings. Looking for general location via IP address...')
    log.debug('Calling IPtoGP')
    findAddress = getByIP()
    settings['applets']['forecast']['settings']['address'].update(findAddress)

else:
    location = settings['applets']['forecast']['settings']['address']

conf.save(settings, existingConfFilepath)

region = location['region']
city = location['city']
zipcode = location['zip']
lat = location['lat']
lon = location['lon']

log.debug('Found location information %s' % location)

wind = False


def refresh_weather():
    global wind
    log.debug('Fetching weather again')
    weather = getWeather(lat, lon, apiKey)
    log.debug('Now updating window')
    mainWin['WCONDITIONSICON'].Update(getIcon(weather['icon']))
    log.debug('Updated conditions icon to %s' % mainWin['WCONDITIONSICON'].Filename)
    mainWin['WSUMMARY'].Update(weather['summary'])
    log.debug('Updated Conditions readout to %s' % mainWin['WSUMMARY'].DisplayText)
    mainWin['temp'].Update(str(weather['temperature']) + ' °' + 'F')
    log.debug('Updated Temp readout to %s' % mainWin['temp'].DisplayText)
    mainWin['realFeel'].Update(str(weather['apparentTemperature']) + ' °' + 'F')
    log.debug('Updated RealFeel readout to %s' % mainWin['realFeel'].DisplayText)

    wind = 'Blowing %s at %s/MpH (Gusting at %s)' % (
        w_bearing,
        weather['windSpeed'],
        weather['windGust']
    )
    mainWin['WWIND'].Update(wind)
    log.debug('Updated wind to: %s' % wind)
    log.debug('Refreshing window...')
    mainWin.Read(timeout=100)
    log.debug('Weather data refresh complete!')


sg.change_look_and_feel(settings['applets']['forecast']['settings']['preferences']['theme'])

log.debug('Looking for darksky API key')
if settings['applets']['forecast']['settings']['api']['darksky']['key']:
    log.debug('Found key')
else:
    log.warning('Did not find key!')
    log.debug('Popping up window to ask user for API key')
    key = sg.PopupGetText('Could not find DarkSky API Key. Please enter it below!', )
    log.debug('User entered %s' % key)
    if key is None:
        log.fatal('User did not provide a key and closed the window')
        exit(1)
    else:
        log.info(key)
        settings['applets']['forecast']['settings']['api']['darksky']['key'] = key

apiKey = settings['applets']['forecast']['settings']['api']['darksky']['key']
conf.save(settings, existingConfFilepath)

weather = getWeather(lat, lon, apiKey)
w_bearing = get_compass(weather['windBearing'])
wind = 'Blowing %s at %s/MpH (Gusting at %s)' % (
    w_bearing,
    weather['windSpeed'],
    weather['windGust']
)

weather_frame = [
    [sg.Text('Conditions', justification='center', key='WCONDITIONSLABEL'),
     sg.Image(getIcon(weather['icon']), key='WCONDITIONSICON', pad=((25, 50), (0, 0))),
     sg.Text(weather['summary'], key='WSUMMARY', justification='center')],
    [sg.Text('Temp:', justification='left'), sg.VerticalSeparator(pad=((105, 100), (0, 0))),
     sg.Text(str(weather['temperature']) + ' °' + 'F', key='temp')],
    [sg.Text('Feels Like:', justification='left'), sg.VerticalSeparator(pad=((72, 100), (0, 0))),
     sg.Text(str(weather['apparentTemperature']) + ' °' + 'F', key='realFeel')],
    [sg.Text('Wind:', justification='left'), sg.VerticalSeparator(pad=((109, 100), (0, 0))),
     sg.Text(wind, key='WWIND')],
    [sg.Button('Refresh')]
]
appMenu = [['Settings', ['Location', 'Weather API']]]

layout = [
    [sg.Menu(appMenu)],
    [sg.Frame('Current Weather', weather_frame, font='Any 18', title_color='blue')],
    [sg.Button('OK')]
]

mainWin = sg.Window('adaForecast', layout, size=[800, 600])
prefWinActive = False
localeWinActive = False
wPrefsWinActive = False

while True:
    event, values = mainWin.Read(timeout=100)
    if event is None:
        log.info('User exited the app')
        mainWin.Close()
        exit()

    if event == 'Refresh':
        log.debug('User refreshed the weather info')
        refresh_weather()

    if not localeWinActive and event == 'Location':
        localeWinActive = True
        log.debug('User entered the location window')

        if location['lat']:
            guiLat = location['lat']
            guiLng = location['lon']

        else:
            guiLat = ''
            guiLng = ''

        localeWinLayout = [
            [sg.Text('Location Information', size=(30, 1), justification='center', font=("Helvetica", 25),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Frame(layout=[
                [sg.Text('Latitude', justification='left'), sg.InputText(guiLat, key='_LAT_')],
                [sg.Text('Longitude', justification='left'), sg.InputText(guiLng, key='_LON_')]], title='Coordinates',
                relief=sg.RELIEF_SUNKEN, tooltip='Put your GPS cords here')],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]

        localeWin = sg.Window('adaForecast-Location Settings', localeWinLayout)

    if localeWinActive:
        localeEvent, localeVal = localeWin.Read(timeout=100)
        if localeEvent is None or localeEvent == 'Cancel':
            localeWinActive = False
            localeWin.Close()

        if localeEvent is 'OK':
            settings['applets']['forecast']['settings']['address']['lat'] = str(localeVal['_LAT_'])
            log.debug('Latitude set to: %s' % localeVal['_LAT_'])
            settings['applets']['forecast']['settings']['address']['lon'] = str(localeVal['_LON_'])
            log.debug('Longitude set to %s' % localeVal['_LON_'])
            log.debug('Saving new location settings')
            conf.save(settings, existingConfFilepath)
            localeWin.Close()

    if not wPrefsWinActive and event == 'Weather API':
        wPrefsWinActive = True
        log.debug('User entered the Weather API Preferences window')

        if settings['applets']['forecast']['settings']['api']['darksky']['key']:
            user_key = apiKey
        else:
            user_key = 'None'

        wPrefsWinLayoutFrame = [
            [sg.Text('API Key:'), sg.InputText(user_key), sg.Button('Test', disabled=True)],
            [sg.Text('Is key valid?'), sg.Image(conn_image(check_key(user_key)))]
        ]

        wPrefsWinLayout = [
            [sg.Frame('API Settings', wPrefsWinLayoutFrame, font='Any 18', title_color='blue')],
            [sg.Submit(), sg.Cancel()]
        ]
        wPrefsWin = sg.Window('Weather Preferences', wPrefsWinLayout)

    if wPrefsWinActive:
        wPrefsEvent, wPrefsVal = wPrefsWin.Read(timeout=100)
        if wPrefsEvent is None or wPrefsEvent == 'Cancel':
            wPrefsWinActive = False
            wPrefsWin.Close()

mainWin.close()
