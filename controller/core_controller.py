# coding=utf-8
import re
import json
import urllib
import urllib2
from the_project import PROJECT_DIR
from model.key_manager import KeyManager
from model.bot_manager import BotManager


class CoreController(object):
    def __init__(self):
        with open('{}/controller/conf.json'.format(PROJECT_DIR)) as f:
            self.conf = json.load(f)
            self.key_manager = KeyManager()
            self.bot_manager = BotManager()

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
            match = re.findall(r'^<(.*?)> 2FA Token: (\w{5}?)$', the_text)
            for i in match:
                res_list.append('2fa {}'.format(' '.join(i)))

        def _owns_receiver():
            match = re.findall(r'^<(.*?)> 2FA Token: (.....?)$', the_text)
            for i in match:
                res_list.append('2fa {}'.format(' '.join(i)))

        res_list = []
        _2fa_receiver()
        _owns_receiver()
        pass


if __name__ == '__main__':
    cc = CoreController()
    res = cc.connector('owns marymale0 *')
    print res
    cc.receiver(res)
    # cc.bot_manager.get_all_bot_name()
    pass
