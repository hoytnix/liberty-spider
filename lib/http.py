import sys

import requests

from lycosidae.settings import SETTINGS
from lib.urls import sanitize_url


def download(url, file_path=None, original_url=None):
    try:
        url = sanitize_url(url, origin=original_url)

        headers = {'User-Agent': 'Mozilla/5.0 (compatible)'}

        r = requests.get(url, headers=headers, timeout=SETTINGS['HTTP_TIMEOUT_SECS'])
        html = r.content

        if file_path:
            with open(file_path, 'wb+') as f:
                f.write(html)
            return file_path

        return html.decode('utf-8', errors='ignore')

    # Ignore all these exceptions.
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False
    except requests.exceptions.TooManyRedirects:
        return False

    # Capture the rest.
    except:
        print(sys.exc_info()[0], 'ORIGINAL', original_url, 'ACTUAL', url)
        return False
