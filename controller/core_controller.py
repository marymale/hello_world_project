# coding=utf-8
import re
import json
import urllib
import urllib2
from the_project import PROJECT_DIR


class CoreController(object):
    def __init__(self):
        with open('{}/controller/conf.json'.format(PROJECT_DIR)) as f:
            self.conf = json.load(f)

    def connector(self, command):
        text = urllib.urlencode({'command': command})
        req = urllib2.Request(url='{}?{}'.format(self.conf['url'], text))
        return urllib2.urlopen(req).read().strip()

    @staticmethod
    def transmitter(the_text):
        pass

    @staticmethod
    def receiver(the_text):
        def _2fa_receiver():
            print

        pass


if __name__ == '__main__':
    cc = CoreController()
    print cc.connector('2fa marymale1')
    pass
