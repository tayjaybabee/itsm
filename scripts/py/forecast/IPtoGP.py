""" Get geolocation via IP address by accessing IP-API.com """

import requests
from scripts.py.application import logger

name = 'IPtoGP'

log = logger.setup_logger(name)


def getByIP():
    service = 'ip-api.com'
    ip2gpURL = 'http://ip-api.com/json/?fields=city,zip,lat,lon,timezone,isp,region'
    log.info('Checking for general location via user\'s IP Address with %s' % service)
    res = requests.get(ip2gpURL)
    if res.status_code == 200:
        return res.json()
