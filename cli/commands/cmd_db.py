import click

from lycosidae.database import Base, engine, session
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
    
    # Delete
    from lib.paths import database_path
    with open(database_path, 'w+') as stream:
        pass

    # Create tables
    Base.metadata.create_all(engine)

    # Seed
    new_site = Site(url='http://hoyt.io')
    session.add(new_site)
    session.commit()
    session.refresh(new_site)
    session.close()


@click.command()
def seed():
    """ Seeds the database. """
    new_site = Site(url='http://hoyt.io')
    session.add(new_site)
    session.commit()
    session.refresh(new_site)
    session.close()


cli.add_command(init)
cli.add_command(reset)
cli.add_command(seed)
