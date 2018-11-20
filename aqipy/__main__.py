import click
import json
import os
import requests


@click.command()
@click.argument('geo', required=False)
@click.option('--latlon', '-l', help='Format: Latitude;Longitude')
def main(geo, latlon):
    """A simple command line tool to find Air Quality Indices (AQI)
    from around the world."""

    try:
        api_token = os.environ['AQIPY_TOKEN']
        payload = {'token': api_token}
    except:
        print('ERROR: You must set AQIPY_TOKEN environment variable.')
        return

    base_url = 'http://api.waqi.info/feed/'

    if geo:
        if not latlon:
            latlon = input("Enter decimal lat and lon in the form: lat;lon: ")
        url = f'{base_url}geo:{latlon}/'
        location, aqi = api_request(url, payload)
        print(f'The AQI at {location} is {aqi}.')
    else:
        url = f'{base_url}here/'
        location, aqi = api_request(url, payload)
        print(f'The AQI at {location} is {aqi}.')


def api_request(url, payload):
    r = requests.get(url, payload)
    response = r.json()
    location = response['data']['city']['name']
    aqi = response['data']['aqi']
    return location, aqi


if __name__ == '__main__':
    main()
