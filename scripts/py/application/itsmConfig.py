from scripts.py.application import logger
import commentjson
from os import path

name = 'ITSMConfig'

log = logger.setup_logger(name)


def readConf(file):
    if path.exists(path.abspath(file)):
        log.debug('Found %s' % file)
        load_conf = file
    else:
        log.fatal('Please check documentation')

    with open(load_conf, 'r') as confInfo:
        info = commentjson.loads(confInfo.read())

        return info



def save(conf):
    global log
    log.info('Received request to save config file')

    with open(conf_filename, 'w') as confFile:
        import json
        json.dump(config, confFile)
    log.info('Saved!')