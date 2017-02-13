import click

from lycosidae.app import loop


@click.command()
def cli():
    """Run the program."""
    loop()
