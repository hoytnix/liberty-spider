import click

from lycosidae.database import Base, engine
from lycosidae.models.site import Site


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
def init():
    """ Initialize the database. """
    Base.metadata.create_all(engine)

    return None

@click.command()
def reset():
    """ Deletes the current database and creates new tables. """
    from lib.paths import database_path
    with open(database_path, 'w+') as stream:
        pass
    Base.metadata.create_all(engine)

    return None



cli.add_command(init)
cli.add_command(reset)