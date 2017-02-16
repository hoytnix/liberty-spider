import click

from lycosidae.database import Base, engine, session


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
    
    # Import
    from lycosidae.models.site import Site

    print("Imported.")

    # Delete
    Base.metadata.drop_all(engine)

    print("Deleted.")

    # Create tables
    Base.metadata.create_all(engine)

    print("Created.")

    # Seed
    Site.insert(url='https://ma.tt')

    print("Populated.")


cli.add_command(init)
cli.add_command(reset)
