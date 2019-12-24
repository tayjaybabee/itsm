from scripts.py.application import logger
import commentjson
from os import path

name = 'ITSMConfig'

log = logger.setup_logger(name)


def save(settings, conf_filename):
    global log
    log.info('Received request to save config file')

    with open(conf_filename, 'w') as confFile:
        import json
        json.dump(settings, confFile)
    log.info('Saved!')


def readConf(file):
    if path.exists(path.abspath(file)):
        log.debug('Found %s' % file)
        load_conf = file
    else:
        log.fatal('Please check documentation')

    with open(load_conf, 'r') as confInfo:
        info = commentjson.loads(confInfo.read())

        return info




