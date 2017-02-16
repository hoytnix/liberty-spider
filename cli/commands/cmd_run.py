import click

from lycosidae.app import Lycosidae
from lycosidae.settings import SETTINGS


@click.command()
@click.option('--concurrency', default=-1, type=int)
def cli(concurrency):
    """Run the program."""
    if concurrency > -1:
        SETTINGS['ENGINE_CONCURRENCY'] = concurrency

    Lycosidae()