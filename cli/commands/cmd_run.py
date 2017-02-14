import click

from lycosidae.app import Lycosidae


@click.command()
def cli():
    """Run the program."""
    Lycosidae()
