from time import strftime, sleep
from imp import reload

import click


@click.command()
@click.option('--frequency', '-f', default=60, type=int)
def cli(frequency):
    """Run the program."""
    update_increment_seconds = frequency

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

        log_str = ( "{time} {count} {average:.2f} p/s".format(
                        time=strftime('%H:%M:%S'),
                        count=last_count,
                        average=average
        ) )
        print(log_str)

        print(techs())
        print('-' * 20)
        
        sleep(update_increment_seconds)

def count():
    # Ensures an updated session count!
    from lycosidae import database
    database = reload(database)

    from lycosidae.models.site import Site

    return database.session.query(Site).count()

def techs():
    from lycosidae import database
    database = reload(database)

    from lycosidae.models.site import Site, site_technologies
    from lycosidae.models.technology import Technology

    sites_visited = database.session.query(Site).filter(Site.last_checked.isnot(None)).count()

    l = []
    technologies = database.session.query(Technology).all()
    for t in technologies:
        q = database.session.query(site_technologies).filter_by(technology_id=t.id).count()
        a = (q / sites_visited) * 100
        l.append('{} {} {:.2f}%'.format(q, t.title, a))
    return '\n'.join(l)