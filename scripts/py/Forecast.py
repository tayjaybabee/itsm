import PySimpleGUI as sg
import requests
import commentjson
import os.path as path
from scripts.py.application import logger

name = 'adaForecast'
config = {}
settings = {}
apiKey = ''
darkSkyURL = 'https://api.darksky.net/forecast/'

log = logger.setup_logger(name)
log.info('The logger is awake')
log.debug('Determining where in the filesystem I am')

appPath = path.dirname(path.abspath(__file__))
log.debug(' Found path: %s' % appPath)

mediaDir = path.abspath(appPath + '/media')
imagesDir = path.abspath(mediaDir + '/images')

def check_key():
    light =
    test_url = darkSkyURL + apiKey + '/37.8267,-122.4233'
    res = requests.get(test_url)
    if res:
        log.info('Valid key!')
    else:
        log.warning('Invalid key!')
        log.debug('Popping popup to advise user of this')
        sg.PopupError('Invalid key!')


confPath = path.abspath(appPath + '/forecast/conf')
log.info(' Checking for config file in %s' % confPath)
existingConfFilepath = path.abspath(confPath + '/forecast_conf.json')
log.debug(' Looking for %s' % existingConfFilepath)

if path.exists(confPath + '/forecast_conf.json'):
    confFile = path.abspath(confPath + '/forecast_conf.json')
else:
    confFile = path.abspath(confPath + '/example_forecast_conf.json')

    with open(confFile, 'r') as confInfo:
        info = commentjson.loads(confInfo.read())
        config.update(info)
        settings = config['applets']['forecast']['settings']
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


layout = [
    [sg.Menu(appMenu)],
    [sg.Text('Welcome to adaForecast!')],
    [sg.Text('Connection Status:'), sg.Image(imagesDir + '/light_on.png', key='_STATUS_')],
    [sg.Button('OK')]
]

def load_config():
    global config



mainWin = sg.Window('adaForecast', layout)
prefWin_active = False
localeWin_active = False

while True:
    event, values = mainWin.read()
    if event is None:
        log.info('User exited the app')
    else:
        log.info('EVENT: '+ event)

    if event in (None, 'Exit'):
        break

mainWin.close()
