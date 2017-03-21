import os

from urllib.parse import urlparse


class URL:
    def __init__(self, location):
        self.fqu = None
        self.tld = None
        self.domain = None
        self.scheme = None

        location = location.lower()

        # Catch IPv6 errors
        try:
            urlparse(location)
        except ValueError:
            pass

        if '://' in location:
            self.scheme = location.split('://')[0]

        tlds_one, tlds_two = self.tld_list()
        o = location.replace(self._scheme, '').split('/')[0]
        for extension in tlds_two:
            if o.endswith(extension):
                self.tld = extension
                break

        if not self.tld:
            for extension in tlds_one:
                if o.endswith(extension):
                    self.tld = extension
                    break

        if self.tld:
            self.domain = location.replace(self._scheme, '').split(self.tld)[0].split('.')[-1] + self.tld

        if self.domain:
            self.fqu = (self._scheme or 'http://') + self.domain + self.tld

    @property
    def _scheme(self):
        try:
            return self.scheme + '://'
        except:
            return ''

    @classmethod
    def tld_list(cls):
        cwd = os.path.dirname(os.path.abspath(__file__))
        _dir = os.path.join(cwd, 'tlds')

        all_tlds = []
        for (root, _, file_names) in os.walk(_dir):
            for file_name in file_names:
                fp = os.path.join(root, file_name)
                with open(fp, 'r') as stream:
                    for line in stream:
                        all_tlds.append(line.strip())
        all_tlds = set(all_tlds)

        two_levels = []
        one_level = []
        for extension in all_tlds:
            if extension.split('.').__len__() == 2:
                two_levels.append('.' + extension)
            else:
                one_level.append('.' + extension)

        return ((
            sorted(one_level, key=len, reverse=True), 
            sorted(two_levels, key=len, reverse=True)
        ))