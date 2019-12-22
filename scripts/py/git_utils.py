#! /usr/bin python3

import commentjson
from github import Github
import logging as log
import os
import PySimpleGUI as sg
import requests

log.basicConfig(level=log.DEBUG)
log.info('Successfully started logger!')

sg.change_look_and_feel('LightBrown13') # Supposedly the default sucks
                                       # per PySimpleGUI docs


currentPath = os.path.dirname(os.path.abspath(__file__))

conf_path = False

username = ''
config = {}
conf_filename = currentPath + '/git_utils/conf/git_utils_conf.json'


def check_username(self, uname):
    res = requests.get('https://github.com' + uname)
    if res.status_code == 200:
        return True
    else:
        return False


def read_conf():

    global config
    global currentPath
    global username
    global conf_path
    global conf_filename
    conf_dir = '%s/git_utils/conf/' % currentPath
    conf_file = '%s%s' % (conf_dir, conf_filename) # You're a wizard, harry
    fallback_file = '%sexample_git_utils_conf.json' % conf_dir

    if os.path.exists(conf_file):
        conf_path = conf_file
    else:
        conf_path = fallback_file

    with open(conf_path, 'r') as confInfo:
        info = commentjson.loads(confInfo.read())
        config.update(info)
        username = config['auth']['user']['name']
        if username == 'null':
            username = 'Unknown user'
        elif not check_username(uname=username):
            username = 'Unknown user'



def save_conf():
    global config
    global log
    log.info('Received request to save config file')

    with open(conf_filename, 'w') as confFile:
        import json
        json.dump(config, confFile)
    log.info('Saved!')


def parse_save_prefs(preferences):
    print(preferences)
    if preferences[0]:
        config['prefs']['grabAnywhere'] = True
    else:
        config['prefs']['grabAnywhere'] = False

    save_conf()

read_conf()


# Define an application menu
menu = [['Application', ['Preferences', 'Debugger', 'Themes']]]


# Let's put our things that we need for our window in a list!

layout = [[sg.Menu(menu)],
          [sg.Text('User'), sg.Text(username, key='_USERNAME_')],
          [sg.Button('Login'), sg.Button('Exit')]]


# Okay Window, I've packed your layout...
# ....showtime!
mainWin = sg.Window('ITSM - GitUtils', layout, grab_anywhere=config['prefs']['grabAnywhere'])
logWin_active = False
prefWinActive = False

# Loop-de-loop until the end-user submits or breaks....
# I mean exits.
while True:
    global prefs
    ev1, vals1 = mainWin.Read(timeout=100)
    if ev1 is None or ev1 == 'Exit':
        break

    if not logWin_active and ev1 == 'Login':
        logWin_active = True
        logWinLayout = [
            [sg.Text('Username', size=(15, 1)), sg.InputText('', key='Username')],
            [sg.Text('Password', size=(15, 1)), sg.InputText('', key='Password', password_char='*')],
            [sg.Checkbox('Remember me', default=False)],
            [sg.Button('Login'), sg.Button('Cancel')]
        ]

        logWin = sg.Window('Github Login', logWinLayout, grab_anywhere=config['prefs']['grabAnywhere'])

    if logWin_active:
        ev2, vals2 = logWin.Read(timeout=500)
        if ev2 is None or ev2 == 'Cancel':
            logWin_active = False
            logWin.Close()
        if ev2 == 'Login':
            gh = Github(vals2['Username'], vals2['Password'])
            print(gh.get_repos)
            if gh:
                logWin.close()
            mainWin.Element('_USERNAME_').Update(vals2['Username'])

    if ev1 == 'Preferences':
        prefWinActive = True
        prefWinLayout = [
            [sg.Text('User Interface:', size=(15, 1))],
            [sg.Checkbox('Grab anywhere to move windows', default=config['prefs']['grabAnywhere'])],
            [sg.VerticalSeparator()],
            [sg.Button('Accept'), sg.Button('Apply'), sg.Button('Cancel')]
        ]
        read_conf()
        sg.show_debugger_popout_window(location=(1, 1))
        prefWin = sg.Window('GitUtils Preferences', prefWinLayout, grab_anywhere=config['prefs']['grabAnywhere'])

    if ev1 == 'Debugger':
        sg.show_debugger_popout_window(location=(1, 1))

    if ev1 == 'Themes':
        sg.preview_all_look_and_feel_themes()

    if prefWinActive:
        ev3, vals3 = prefWin.Read(timeout=500)
        if ev3 is None or ev3 == 'Cancel':
            prefWinActive = False
            prefWin.Close()
        if ev3 == 'Accept':
            log.info('User clicked accept in prefs window')
            parse_save_prefs(vals3)
            prefWin.Close()
            mainWin.refresh()
        if ev3 == 'Apply':
            log.info('User clicked apply in prefs window')
            parse_save_prefs(vals3)
            prefWin.refresh()
            mainWin.refresh()


# Bye!
mainWin.close()
