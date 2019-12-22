import requests

def get_GP():
    api_url = 'http://ip-api.com/json/?fields=city,zip,lat,lon,timezone,isp'
    response = requests.get(api_url)
    return response.json()