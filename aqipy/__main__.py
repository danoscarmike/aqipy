import click
import json
import os
import requests


@click.command()
@click.argument('geo', required=False)
@click.option('--latlon', '-l', help='Format: Latitude;Longitude')
def main(geo):
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
        latlon = click.prompt("Enter decimal lat and lon in the form: lat;lon")
        url = f'{base_url}geo:{latlon}/'
        location, aqi, attribs = api_request(url, payload)
        print(f'\nThe AQI at {location} is {aqi}.\n')
        print_attributions(attribs)
    else:
        url = f'{base_url}here/'
        location, aqi, attribs = api_request(url, payload)
        print(f'\nThe AQI at {location} is {aqi}.\n')
        print_attributions(attribs)


def print_attributions(attribs):
    print('With thanks to:')
    i = 0
    while i < len(attribs)-2:
        print(f'{attribs[i]["name"]},')
        i += 1
    print(f'{attribs[-2]["name"]}, and')
    print(f'{attribs[-1]["name"]}.\n')


def api_request(url, payload):
    r = requests.get(url, payload)
    response = r.json()
    location = response['data']['city']['name']
    aqi = response['data']['aqi']
    attribs = response['data']['attributions']
    return location, aqi, attribs


if __name__ == '__main__':
    main()
