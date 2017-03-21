from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lib.http import download

class Profiler(dict):
    def __init__(self, html):
        self.html = html.lower()

        self.d = {}
        for x in dir(self):
            if x.startswith('_Profiler__'):
                k = x.replace('_Profiler__', '')
                v = getattr(self, x)()
                self.d[k] = v
    
    def check(self, keys):
        for key in keys:
            if key in self.html:
                return True

    def __wordpress(self):
        keys = ['wp-content',
                'wp-includes',
                'wp-admin']
        return self.check(keys)
    
    def __google_analytics(self):
        keys = ['google-analytics.com/ga.js'
                'google-analytics.com/analytics.js']
        return self.check(keys)
    
    def __clicky_analytics(self):
        keys = ['getclicky.com']
        return self.check(keys)
    
    def __woocommerce(self):
        keys = ['class="woocommerce']
        return self.check(keys)
    
    def __stripe(self):
        keys = ['js.stripe.com']
        return self.check(keys)
    
    def __optimizely(self):
        keys = ['cdn.optimizely.com/js']
        return self.check(keys)
    
    def __crazy_egg(self):
        keys = ['script.crazyegg.com']
        return self.check(keys)
    
    def __mixpanel(self):
        keys = ['cdn.mxpnl.com']
        return self.check(keys)
    
    def __kissmetrics(self):
        keys = ['i.kissmetrics.com/i.js']
        return self.check(keys)
    
    def __infusionsoft(self):
        keys = ['infusionsoft.com/app/webTracking/getTrackingCode']
        return self.check(keys)

    def _yoast_seo(self):
        keys = ['yoast seo plugin']
        return self.check(keys)

    def __doubleclick(self):
        keys = ['client="ca-pub-']
        return self.check(keys)

    def __hubspot(self):
        keys = ['js.hs-scripts.com']
        return self.check(keys)

    def __hotjar(self):
        keys = ['h,o,t,j,a,r']
        return self.check(keys)