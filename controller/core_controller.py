# coding=utf-8
import re
import json
import requests
from Crypto.Cipher import AES
from the_project import PROJECT_DIR
from model.key_manager import KeyManager
from model.bot_manager import BotManager


class CoreController(object):
    def __init__(self):
        with open('{}/controller/conf.json'.format(PROJECT_DIR)) as f:
            self.conf = json.load(f)
        self.encryption = AES.new('marymale key2333', AES.MODE_CBC, 'This is marymale')
        self.key_manager = KeyManager()
        self.bot_manager = BotManager()
        self.req_text = ''
        self.res_text = ''

    def connector(self, command):
        url = self.conf['url']
        d = {'command': command}
        r = requests.post(url, data=d)
        self.res_text = r.text.strip()

    def transmitter(self, _blueprint):
        def _2fa():
            op, bot_name = _blueprint.split(' ')[1:3]
            op_dict = {'1': '2fa', '2': '2faok', '3': '2fano'}
            return '{} {}'.format(str(op_dict[op]), str(bot_name))

        def _owns():
            bot_name, game_id = _blueprint.split(' ')[1:3]
            return 'owns {} {}'.format(bot_name, game_id)

        run_dict = {'2fa': _2fa, 'owns': _owns}

        self.req_text = self.encryption.encrypt(run_dict[_blueprint.split(' ')[0]]())

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

        print res_list

    def generator(self, blueprint):
        self.transmitter(blueprint)
        self.connector(self.req_text)
        self.receiver(self.res_text)


if __name__ == '__main__':
    cc = CoreController()
    cc.generator('owns marymale0 *')
    print cc.req_text
    print cc.res_text
    # cc.connector('2fa marymale0')
    # print cc.res_text
    # cc.receiver(res)
    # cc.bot_manager.get_all_bot_name()
    pass
