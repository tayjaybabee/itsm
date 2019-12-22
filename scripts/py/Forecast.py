import PySimpleGUI as sg
import requests
import commentjson
import os.path as path
from scripts.py.application import logger

name = 'adaForecast'
apiKey = ''
darkSkyURL = 'https://api.darksky.net/forecast/'
connLight = False

sg.change_look_and_feel('DarkAmber')

log = logger.setup_logger(name)
log.info('The logger is awake')

from scripts.py.application import itsmConfig as config
log.debug('Determining where in the filesystem I am')

appPath = path.dirname(path.abspath(__file__))
log.debug(' Found path: %s' % appPath)

confPath = path.abspath(appPath + '/forecast/conf')

existingConfFilepath = path.abspath(confPath + '/forecast_conf.json')

if path.exists(confPath + '/forecast_conf.json'):
    confFile = path.abspath(confPath + '/forecast_conf.json')
else:
    confFile = path.abspath(confPath + '/example_forecast_conf.json')
config.readConf(confFile)

mediaDir = path.abspath(appPath + '/media')
imagesDir = path.abspath(mediaDir + '/images')

def check_key():
    global connLight, log
    log.debug('Checking provided key')

    test_url = darkSkyURL + apiKey + '/37.8267,-122.4233'
    res = requests.get(test_url)
    if res:
        log.info('Valid key!')
        connLight = True
    else:
        log.warning('Invalid key!')
        log.debug('Popping popup to advise user of this')
        sg.PopupError('Invalid key!')
        connLight = False


settings = config.readConf(confFile)['applets']['forecast']['settings']
cords = False
address = False


def getByIP():
    service = 'ip-api.com'
    ip2gpURL = 'http://ip-api.com/json/?fields=city,zip,lat,lon,timezone,isp,region'
    log.info('Checking for general location via user\'s IP Address with %s' % service)
    res = requests.get(ip2gpURL)
    if res.status_code == 200:
        return res.json()




def determine_cords():
    global settings, log, address, cords
    conf_locale = settings['location']
    conf_addr = conf_locale['address']

    log.debug('Checking to see if user has locale set...')
    if conf_locale['lat']:
        log.debug('Found entry for latitude, looking for longitude')
        if conf_locale['lon']:
            log.debug('Found entry for longitude')
            log.debug('Feeding list containing [lat, lng] to \'cords\' ')
            cords += [conf_locale['lat'], conf_locale['lon']]
        else:
            log.warning('Found latitude in config file but not longitude, ignoring both')
            cords = False

    else:
        log.warning('Could not find an entry for user\'s latitude')
        cords = False



if not cords:
    addy = getByIP()
    settings = settings['location']
    print(addy)
    result = {}
    for key in (settings.viewkeys() | addy.keys()):
        if key in settings: result.setdefault(key, []).append(settings[key])
        if key in addy: result.setdefault(key, []).append(addy[key])

   print(result)



print(settings)


log.debug('Looking for darksky API key')
apiKey = settings['api']['darksky']['key']
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

check_key()


appMenu = [['Settings', ['Location']]]

if connLight:
    lightImage = imagesDir + '/light_on.png'
else:
    lightImage = imagesDir + '/light_off.png'

layout = [
    [sg.Menu(appMenu)],
    [sg.Text('Welcome to adaForecast!')],
    [sg.Text('Connection Status:'), sg.Image(lightImage, key='_STATUS_')],
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

    if not localeWinActive and event == 'Location':
        localeWinActive = True
        log.debug('User entered the location window')

        if cords:
            guiLat = cords[0]
            guiLng = cords[1]
        else:
            guiLat = ''
            guiLng = ''

        localeWinLayout = [
            [sg.Text('Location Information', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [sg.Frame( layout = [
                [sg.Text('Latitude', justification='left'), sg.InputText(guiLat,  key='_LAT_')],
                [sg.Text('Longitude', justification='left'), sg.InputText(guiLng,  key='_LNG_')]], title='Coordinates', relief=sg.RELIEF_SUNKEN, tooltip='Put your GPS cords here')],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]

        localeWin = sg.Window('adaForecast-Location Settings', localeWinLayout)

    if localeWinActive:
        localeEvent, localeVal = localeWin.Read(timeout=100)
        if localeEvent is None or localeEvent == 'Cancel':
            localeWinActive = False
            localeWin.Close()

mainWin.close()
