import logger

name = ITSMApp.ITSMConfig

log = logger.setup_logger(name)
log.info('The logger is awake')


def save(conf):
    global log
    log.info('Received request to save config file')

    with open(conf_filename, 'w') as confFile:
        import json
        json.dump(config, confFile)
    log.info('Saved!')