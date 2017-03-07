import logging

from lib.paths import log_path


# Configure other packages
logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)

# My package
logging.basicConfig(filename=log_path, level=logging.DEBUG)
logger = logging.getLogger(__name__)