import click

from lib.urls import sanitize_url, URL


@click.command()
def cli():
    """Run the program."""
    urls = [
        #'newyorkeronthetown.com/acura//com.om',
        #'oscars/best-picture-box-office/',
        #'www.amazon.com/dreamland-true-americas-opiate-epidemic/',
        '//ma.tt',
        #'#hello-world',
        #'?hello',
        #'/?hello'
    ]

    for url in urls:
        u = URL(location=url)
        