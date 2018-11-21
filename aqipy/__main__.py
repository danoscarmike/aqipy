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
        api_request(url, ctx.obj['TOKEN'])


def validate_latlon(ctx, param, value):
    try:
        lat, lon = value[0], value[1]
        return(lat.strip()+';'+lon.strip())
    except ValueError:
        raise click.BadParameter('latlon must be in format "lat lon"')


@main.command()
@click.pass_context
@click.option('--latlon', '-l',
              callback=validate_latlon,
              help='Format: Latitude, Longitude',
              nargs=2,
              prompt='Enter decimal latitude and longitude <lat lon>'
              )
def geo(ctx, latlon):
    url = f'{ctx.obj["BASE_URL"]}geo:{latlon}/'
    api_request(url, ctx.obj['TOKEN'])


def echo_attributions(attribs):
    print(f'With thanks to {attribs[-1]["name"]}, ', end="", flush=True)
    i = 0
    while i < len(attribs)-2:
        print(f'{attribs[i]["name"]}, ', end="", flush=True)
        i += 1
    print(f'and {attribs[-2]["name"]}.\n')


def api_request(url, payload):
    r = requests.get(url, params=payload)
    response = r.json()
    location = response['data']['city']['name']
    aqi = response['data']['aqi']
    time = response['data']['time']['s']
    tz = response['data']['time']['tz']
    attribs = response['data']['attributions']

    click.echo(f'\nThe AQI at {location} is {aqi}.')
    click.echo(f'Updated at {time} {tz}\n')
    echo_attributions(attribs)
