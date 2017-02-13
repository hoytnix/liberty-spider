from os import path
from os import walk


def all_tlds():
    cwd = path.dirname(path.abspath(__file__))
    _dir = path.join(cwd, 'tlds')

    x = []
    for (root, _, file_names) in walk(_dir):
        for file_name in file_names:
            fp = path.join(root, file_name)
            with open(fp, 'r') as stream:
                for line in stream:
                    x.append(line.strip())
    return set(x)

def clean(url):
    # Fragment
    if url.startswith('#'):
        return False

    # Relative scheme
    if url.startswith('//'):
        url = 'http:' + url

    # Relative link
    if url.startswith('/'):
        return False

    # Irrelevant schemes
    blacklist = ['mailto:', 'ftp:']
    for scheme in blacklist:
        if url.startswith(scheme):
            return False

    # Remember the scheme
    scheme = url.split('//')[0] + '//'
    url = url.replace(scheme, '')

    # Remove the path
    url = url.split('/')[0]

    # Figure out the tld
    two_levels = []
    one_level = []
    for extension in all_tlds():
        if extension.split('.').__len__() == 2:
            two_levels.append(extension)
        else:
            one_level.append(extension)
    
    domain_tld = None
    for extension in two_levels:
        if url.endswith(extension):
            domain_tld = extension
            break

    if not domain_tld:
        for extension in one_level:
            if url.endswith(extension):
                domain_tld = extension
                break

    if not domain_tld:
        return False
    else:
        domain_tld = '.' + domain_tld

    # Strip everything!
    url = url.replace(domain_tld, '')
    domain_name = url.split('.')[-1]

    return scheme + domain_name + domain_tld


if __name__ == '__main__':
    x = clean('https://blog.hoyt.co.uk/hello')
    print(x)