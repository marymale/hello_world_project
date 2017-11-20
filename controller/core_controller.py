# coding=utf-8
import re
import json
import requests
import urllib
from the_project import PROJECT_DIR
from controller.key_controller import KeyController
from controller.bot_controller import BotController


class CoreController(object):
    def __init__(self):
        with open('{}/controller/conf.json'.format(PROJECT_DIR)) as f:
            self.conf = json.load(f)
        self.key_controller = KeyController()
        self.bot_controller = BotController()
        self.req_list = None
        self.res_list = None

    def connector(self):
        self.res_list = list()
        for text in self.req_list:
            command = '{}?{}'.format('http://127.0.0.1:1242/IPC', urllib.urlencode({'command': text}))
            r = requests.post(self.conf['url'], data={'command': command})
            self.res_list.append(r.text)

    def transmitter(self, _blueprint):
        def _2fa():
            bot_name, op = _blueprint.split(' ')[1:3]
            op_dict = {'1': '2fa', '2': '2faok', '3': '2fano'}
            return ['{} {}'.format(str(op_dict[op]), str(bot_name))]

        def _addkey():
            the_text, level, game_id = _blueprint.split(' ')[1:4]
            self.key_controller.add_key_list(the_text, level, game_id)
            return []

        def _addlicense():
            command = list()
            game_id = _blueprint.split(' ')[1]
            for bot_name in self.bot_controller.get_all_bot_names():
                command.append('addlicense {} {}'.format(str(bot_name), str(game_id)))
            return command

        def _owns():
            if _blueprint != 'owns':
                bot_name, game_id = _blueprint.split(' ')[1:3]
                return ['owns {} {}'.format(str(bot_name), str(game_id))]
            else:
                command = list()
                for bot_name in self.bot_controller.get_all_bot_names():
                    command.append('owns {} *'.format(str(bot_name)))
                return command

        def _cmd():
            commend = ' '.join(_blueprint.split(' ')[1:])
            return [commend]

        run_dict = {'2fa': _2fa, 'owns': _owns, 'addkey': _addkey, 'addlicense': _addlicense, 'cmd': _cmd}
        self.req_list = run_dict[_blueprint.split(' ')[0]]()

    def receiver(self):
        def _2fa_receiver(the_text):
            pattern = r'^<(.+?)> 2FA Token: (\w{5}?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': '2fa', 'bot_name': i[0], '2fa_id': i[1]}
                    res_list.append(item)

            pattern = r'^<(.+?)> Success!\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                item = {'op': '2fa_success', 'bot_name': match[0]}
                res_list.append(item)

        def _owns_receiver(the_text):
            pattern = r'^<(.+?)> Owned already: (\w+?) \| (.+?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'owns', 'bot_name': i[0], 'game_id': i[1], 'game_name': i[2].encode('utf-8')}
                    res_list.append(item)

        def _addlicense_receiver(the_text):
            pattern = r'<(.+?)> ID: (.+?) \| Status: (.+?) \| Items: (.+?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'owns', 'bot_name': i[0], 'game_id': i[1], 'status': i[2]}
                    res_list.append(item)

        res_list, res_text_list = list(), list()
        exe_list = [_2fa_receiver, _owns_receiver, _addlicense_receiver]
        for text in self.res_list:
            res_text_list.extend(text.split('\n'))
        for each in res_text_list:
            for exe in exe_list:
                exe(each)

        self.res_list = res_list

    def executor(self):
        def _owns_executor():
            own_list = [i for i in self.res_list if i['op'] == 'owns']
            bot_name_set = set()
            for i in own_list:
                bot_name_set.add(i['bot_name'])
            for bot_name in list(bot_name_set):
                self.bot_controller.update_bot_own_list(bot_name, [i for i in own_list if i['bot_name'] == bot_name])

        _owns_executor()

    def generator(self, blueprint):
        self.transmitter(blueprint)
        self.connector()
        self.receiver()
        self.executor()


if __name__ == '__main__':
    cc = CoreController()
    cc.generator('owns')
    for req in cc.req_list:
        print req
    for res in cc.res_list:
        print res
    # 2fa: 2fa bot_name 1/2/3(2fa,2faok,2fano)
    # addlicense: addlicense game_id
    # own: owns(all)/owns bot_name game_id(*)
    # cmd: origin command
    pass
