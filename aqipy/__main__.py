import click
import json
import os
import requests


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """A simple command line tool to find Air Quality Indices (AQI)
    from around the world."""

    ctx.ensure_object(dict)

    try:
        api_token = os.environ['AQIPY_TOKEN']
        ctx.obj['TOKEN'] = {'token': api_token}
        ctx.obj['BASE_URL'] = 'http://api.waqi.info/feed/'
    except:
        click.echo(f'ERROR: You must set an AQIPY_TOKEN environment variable.')
        return

    if ctx.invoked_subcommand is None:
        url = f'{ctx.obj["BASE_URL"]}here/'
        location, aqi, attribs = api_request(url, ctx.obj['TOKEN'])
        click.echo(f'\nThe AQI at {location} is {aqi}.\n')
        echo_attributions(attribs)


def validate_latlon(ctx, param, value):
    try:
        lat, lon = value.split(',', 2)
        return(lat.strip()+';'+lon.strip())
    except ValueError:
        raise click.BadParameter('latlon must be in format "lat,lon"')


@main.command()
@click.pass_context
@click.option('--latlon', '-l',
              callback=validate_latlon,
              help='Format: Latitude, Longitude',
              prompt='Enter decimal latitude and longitude <lat, lon>'
              )
def geo(ctx, latlon):
    url = f'{ctx.obj["BASE_URL"]}geo:{latlon}/'
    location, aqi, attribs = api_request(url, ctx.obj['TOKEN'])
    print(f'\nThe AQI at {location} is {aqi}.\n')
    echo_attributions(attribs)


def echo_attributions(attribs):
    click.echo('With thanks to:')
    i = 0
    while i < len(attribs)-1:
        print(f'{attribs[i]["name"]},')
        i += 1
    click.echo(f'and {attribs[-1]["name"]}.\n')


def api_request(url, payload):
    r = requests.get(url, params=payload)
    response = r.json()
    location = response['data']['city']['name']
    aqi = response['data']['aqi']
    attribs = response['data']['attributions']
    return location, aqi, attribs
