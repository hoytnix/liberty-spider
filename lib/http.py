import sys

import requests


def download(url, file_path=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible)'
        }

        r = requests.get(url, headers=headers)
        html = r.content

        if file_path:
            with open(file_path, 'wb+') as f:
                f.write(html)
            return file_path

        return html.decode('utf-8', errors='ignore')
    except:
        print("Unexpected error: %s" % sys.exc_info()[0])
        return False
