import click

from lib._urls import URL


@click.command()
def cli():
    urls = ['http://www.httpbin.org/cookies/set/sessioncookie/123456789',
    'https://www.httpbin.co.uk/cookies/set/sessioncookie/123456789#a?b&p',
    'www.httpbin.co.uk/hellow-rold'
    '/hello-world',
    'hello-world',
    '?hello-world',
    '#hello-world']

    for url in urls:
        u = URL(location=url)#, origin='http://google.com/')
        
        print(u.fqu, u.domain)