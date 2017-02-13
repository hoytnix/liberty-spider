from os import path, walk

import anyconfig


def make_settings(environment='develop'):
    """Ordered object for configuration.

    Loops through files in the `configs`-directory by weight, and breaks after 
    it finishes the file which contains the `environment` key.

    Args:
        environment (str): they file-key to break at; defaults to `develop`.

    Returns:
        dict
    """

    cwd = path.dirname(path.abspath(__file__))
    config_dir = path.join(cwd, 'configs')

    config_files = []
    for (root, _, file_names) in walk(config_dir):
        for file_name in file_names:
            config_files.append(path.join(root, file_name))
    config_files = sorted(config_files)

    store = {}
    for config_file in config_files:
        config = anyconfig.load(config_file)
        for key in config:
            store[key] = config[key]

        if environment in config_file:
            break

    return store


try:
    with open(path.join(path.dirname(path.abspath(__file__)), 'env.txt')) as stream:
        ENV = stream.read().strip()
except:
   ENV = None

SETTINGS = make_settings(environment=ENV)
