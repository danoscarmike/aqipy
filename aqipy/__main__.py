import click
import os
import requests

from colored import fg, attr


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """A simple command line tool to find Air Quality Indices (AQI)
    from around the world."""

    ctx.ensure_object(dict)

    try:
        api_token = os.environ["AQIPY_TOKEN"]
        ctx.obj["TOKEN"] = {"token": api_token}
        ctx.obj["BASE_URL"] = "http://api.waqi.info/feed/"
    except KeyError:
        click.echo(
            f"{fg(1)}ERROR:{attr(0)} You must set an AQIPY_TOKEN \
            environment variable."
        )
        click.echo(
            f"Request a token at \
            {fg(12)}https://aqicn.org/data-platform/token/#/{attr(0)}"
        )
        return

    if ctx.invoked_subcommand is None:
        url = f'{ctx.obj["BASE_URL"]}here/'
        api_request(url, ctx.obj["TOKEN"])


def validate_latlon(ctx, param, value):
    try:
        lat, lon = value[0], value[1]
        return lat.strip() + ";" + lon.strip()
    except ValueError:
        raise click.BadParameter('latlon must be in format "lat lon"')


@main.command()
@click.pass_context
@click.option(
    "--latlon",
    "-l",
    callback=validate_latlon,
    help="Format: Latitude, Longitude",
    nargs=2,
    prompt="Enter decimal latitude and longitude <lat lon>",
)
def geo(ctx, latlon):
    url = f'{ctx.obj["BASE_URL"]}geo:{latlon}/'
    api_request(url, ctx.obj["TOKEN"])


def echo_header(location):
    leader_text = "Air quality information for "
    header_len = get_header_len(leader_text, location)
    click.echo()
    click.echo(f'{"-"*header_len}')
    click.echo(f"{leader_text}{location}")
    click.echo(f'{"-"*header_len}')


def get_header_len(leader_text, location):
    leader_len = len(leader_text)
    location_len = len(location)
    return leader_len + location_len


def echo_attributions(attribs):
    click.echo(f"{fg(12)}With thanks to:{attr(0)}")
    click.echo(f'\t{attribs[-1]["name"]}')
    i = 0
    while i < len(attribs) - 1:
        click.echo(f'\t{attribs[i]["name"]}')
        i += 1
    click.echo()


def echo_results(response):
    location = response["data"]["city"]["name"]
    aqi = response["data"]["aqi"]
    dominantpol = response["data"]["dominentpol"]
    dominantpol_level = response["data"]["iaqi"][dominantpol]["v"]
    time = response["data"]["time"]["s"]
    tz = response["data"]["time"]["tz"]
    attribs = response["data"]["attributions"]

    quality, color = aqi_quality(aqi)
    echo_header(location)
    click.echo(f"{fg(12)}The air quality is: {attr(0)}", nl=False)
    click.echo(f"{fg(color)}{quality}{attr(0)}")
    click.echo(f"{fg(12)}The AQI is: {attr(0)}", nl=False)
    click.echo(f"{aqi}")
    click.echo(f"{fg(12)}The dominant pollution is: {attr(0)}", nl=False)
    click.echo(f"{dominantpol} ({dominantpol_level})")
    click.echo(f"{fg(12)}Updated: {attr(0)}", nl=False)
    click.echo(f"{time} {tz}")
    echo_attributions(attribs)


def api_request(url, payload):
    r = requests.get(url, params=payload)
    response = r.json()
    echo_results(response)


def aqi_quality(aqi):
    if aqi < 50:
        return "Good", "light_green"
    if aqi < 100:
        return "Moderate", "light_yellow"
    if aqi < 150:
        return "Unhealthy for sensitive groups", "orange_1"
    if aqi < 200:
        return "Unhealthy", "red"
    if aqi < 300:
        return "Very unhealthy", "dark_magenta_1"
    else:
        return "Hazardous", "dark_red_1"
