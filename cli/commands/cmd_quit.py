import click

from lib.paths import exit_path


@click.command()
def cli():
    """Run the program."""
    with open(exit_path, 'w') as stream:
        stream.write('quit')
