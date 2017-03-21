import sys

import requests
import timeout_decorator

from lycosidae.log import logger
from lycosidae.settings import SETTINGS
from lib._urls import URL


def download(url, file_path=None):
    try:
        url = URL(url).fqu
        if not url:
            return False

        headers = {'User-Agent': 'Mozilla/5.0 (compatible)'}

        r = get(url, headers=headers)
        html = r.content

        if file_path:
            with open(file_path, 'wb+') as f:
                f.write(html)
            return file_path

        return html.decode('utf-8', errors='ignore')

    # Ignore all these exceptions.
    except timeout_decorator.timeout_decorator.TimeoutError:
        return False
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
        print(sys.exc_info()[0], url)
        return False


@timeout_decorator.timeout(SETTINGS['HTTP_TIMEOUT_SECS'], use_signals=False)
def get(url, headers):
    return requests.get(url, headers)