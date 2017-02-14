import sys

import requests

from lycosidae.settings import SETTINGS


def download(url, file_path=None):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible)'}

        r = requests.get(url, headers=headers, timeout=SETTINGS['HTTP_TIMEOUT_SECS'])
        html = r.content

        if file_path:
            with open(file_path, 'wb+') as f:
                f.write(html)
            return file_path

        return html.decode('utf-8', errors='ignore')
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except:
        print("{} {}".format(sys.exc_info()[0], url))
        return False
