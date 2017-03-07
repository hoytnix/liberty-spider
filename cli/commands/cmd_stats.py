from time import strftime, sleep

import click


@click.command()
def cli():
    """Run the program."""
    update_increment_seconds = 120

    last_count = None
    _set = []
    while True:
        if _set.__len__() == 0:
            a = count()
            sleep(update_increment_seconds)
            b = count()
            _set.append(b - a)

            last_count = b
        else:
            c = count()
            _set.append(c - last_count)
            last_count = c

        average = sum(_set) / _set.__len__() / update_increment_seconds
        print(strftime('%H:%M:%S'), last_count, average, 'p/s')
        
        sleep(update_increment_seconds)

def count():
    # Ensures an updated session count!
    from lycosidae.database import session
    from lycosidae.models.site import Site
    return session.query(Site).count()