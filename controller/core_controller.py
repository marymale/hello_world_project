# coding=utf-8
import re
import json
import urllib
import random
import datetime
import requests
import pyperclip
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

    def transmitter(self, _blueprint):
        def _2fa():
            bot_name, op = _blueprint.split(' ')[1:3]
            op_dict = {'1': '2fa', '2': '2faok', '3': '2fano'}
            return ['{} {}'.format(str(op_dict[op]), str(bot_name))]

        # addkey不需要上传命令，返回空指令，因此也没有receiver和executor
        def _addkey():
            the_text, level, game_id, game_name = _blueprint.split(' ')[1:5]
            self.key_controller.add_key_list(the_text, level, game_id, game_name)
            return []

        def _addlicense():
            command = list()
            game_id = _blueprint.split(' ')[1]
            for bot_name in self.bot_controller.get_all_bot_names():
                command.append('addlicense {} {}'.format(str(bot_name), str(game_id)))
            return command

        def _cmd():
            commend = ' '.join(_blueprint.split(' ')[1:])
            return [commend]

        # 暂时不需要
        def _loot():
            pass

        def _owns():
            if _blueprint != 'owns':
                bot_name, game_id = _blueprint.split(' ')[1:3]
                return ['owns {} {}'.format(str(bot_name), str(game_id))]
            else:
                command = list()
                for bot_name in self.bot_controller.get_all_bot_names():
                    command.append('owns {} *'.format(str(bot_name)))
                return command

        def _redeem():
            command = []
            redeem_list = self.key_controller.get_need_redeem_list()
            for i in redeem_list:
                if i[0]['level'] == '2':
                    if i[0]['game_id'] == 'null':
                        command.append('r^ FD {}'.format(','.join([j['key'] for j in i])))
                    else:
                        need_bots = self.bot_controller.get_bot_needs(i[0]['game_id'])
                        random.shuffle(need_bots)
                        redeem_bots = need_bots[:min(len(need_bots), len(i))]
                        for j in range(len(redeem_bots)):
                            command.append('r {} {}'.format(redeem_bots[j], i[j]['key']))
                elif i[0]['level'] == '1':
                    for j in i:
                        command.append('r marymale {}'.format(j['key']))
            print command
            return command

        run_dict = {'2fa': _2fa, 'owns': _owns, 'addkey': _addkey, 'addlicense': _addlicense, 'redeem': _redeem,
                    'cmd': _cmd}
        self.req_list = run_dict[_blueprint.split(' ')[0]]()

    def connector(self):
        self.res_list = list()
        for text in self.req_list:
            command = '{}?{}'.format('http://127.0.0.1:1242/IPC', urllib.urlencode({'command': text}))
            r = requests.post(self.conf['url'], data={'command': command})
            self.res_list.append(r.text)

    def receiver(self):
        def _2fa_receiver(the_text):
            op = False
            pattern = r'^<(.+?)> 2FA Token: (\w{5}?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': '2fa', 'bot_name': i[0], '2fa_id': i[1]}
                    res_list.append(item)
                op = True

            pattern = r'^<(.+?)> Success!\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                item = {'op': '2fa_success', 'bot_name': match[0]}
                res_list.append(item)
                op = True
            return op

        def _addlicense_receiver(the_text):
            op = False
            pattern = r'<(.+?)> ID: (.+?) \| Status: (.+?) \| Items: (.+?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'addlicense', 'bot_name': i[0], 'game_id': i[1], 'status': i[2], 'game_name': i[3]}
                    res_list.append(item)
                op = True
            return op

        def _cmd_receiver(the_text):
            if the_text.strip('\r') not in ['', '<br />']:
                item = {'op': 'cmd', 'text': the_text}
                res_list.append(item)
                return True
            return False

        def _redeem_receiver(the_text):
            op = False
            pattern = r'^<(.+?)> Key: (.{5}-.{5}-.{5}?) \| Status: Fail/AlreadyPurchased \| Items: \[(.+?), (.+?)\]\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'r_AlreadyPurchased', 'bot_name': i[0], 'key': i[1], 'game_id': i[2], 'game_name': i[3]}
                    res_list.append(item)
                op = True

            pattern = r'^<(.+?)> Key: (.{5}-.{5}-.{5}?) \| Status: OK/NoDetail \| Items: \[(.+?), (.+?)\]\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'r_OK', 'bot_name': i[0], 'key': i[1], 'game_id': i[2], 'game_name': i[3]}
                    res_list.append(item)
                op = True

            pattern = r'^<(.+?)> Key: (.{5}-.{5}-.{5}?) \| Status: Fail/DoesNotOwnRequiredApp \| Items: \[(.+?), (.+?)\]\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'r_DoesNotOwnRequiredApp', 'bot_name': i[0], 'key': i[1], 'game_id': i[2], 'game_name': i[3]}
                    res_list.append(item)
                op = True

            pattern = r'^<(.+?)> Key: (.{5}-.{5}-.{5}?) \| Status: Fail/DuplicateActivationCode \| Items: \[(.+?), (.+?)\]\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'r_DuplicateActivationCode', 'bot_name': i[0], 'key': i[1], 'game_id': i[2],
                            'game_name': i[3]}
                    res_list.append(item)
                op = True

            return op

        def _owns_receiver(the_text):
            op = False
            pattern = r'^<(.+?)> Owned already: (\w+?) \| (.+?)\r$'
            if re.match(pattern, the_text) is not None:
                match = re.findall(pattern, the_text)
                for i in match:
                    item = {'op': 'owns', 'bot_name': i[0], 'game_id': i[1], 'game_name': i[2].encode('utf-8')}
                    res_list.append(item)
                op = True
            return op

        res_list, res_text_list = list(), list()
        # _cmd_receiver保持在最后
        exe_list = [_2fa_receiver, _owns_receiver, _addlicense_receiver, _redeem_receiver, _cmd_receiver]
        # DEBUG
        # self.res_list = [pyperclip.paste()]
        for text in self.res_list:
            res_text_list.extend(text.split('\n'))
        for each in res_text_list:
            for exe in exe_list:
                if exe(each):
                    break

        self.res_list = res_list

    def executor(self):
        def _2fa_executor():
            _2fa_list = [i for i in self.res_list if i['op'] == '2fa']
            for i in _2fa_list:
                print '{}:{}'.format(i['bot_name'], i['2fa_id'])
            _2fa_list = [i for i in self.res_list if i['op'] == '2fa_success']
            for i in _2fa_list:
                print '{}:success'.format(i['bot_name'])

        def _addlicense_executor():
            redeem_list = [i for i in self.res_list if i['op'] == 'addlicense']
            for i in redeem_list:
                self.bot_controller.add_bot_own(i['bot_name'], i['game_id'], i['game_name'])
                print 'Addlicense:{}-{}-[{}]'.format(i['bot_name'], i['game_id'], i['game_name'])

        def _redeem_executor():
            redeem_list = [i for i in self.res_list if i['op'] == 'r_OK']
            for i in redeem_list:
                self.key_controller.del_key_by_key(i['key'])
                self.bot_controller.add_bot_own(i['bot_name'], i['game_id'], i['game_name'])
                self.bot_controller.update_bot_available(i['bot_name'], 'Y')
                print 'OK:{}-{}-[{}]'.format(i['bot_name'], i['game_id'], i['game_name'])

            redeem_list = [i for i in self.res_list if i['op'] == 'r_AlreadyPurchased']
            for i in redeem_list:
                self.key_controller.update_key(i['key'], 2, i['game_id'], i['game_name'])
                self.bot_controller.update_bot_available(i['bot_name'], 'Y')

            redeem_list = [i for i in self.res_list if i['op'] == 'r_DuplicateActivationCode']
            for i in redeem_list:
                self.key_controller.del_key_by_key(i['key'])
                self.bot_controller.update_bot_available(i['bot_name'], 'Y')

            redeem_list = [i for i in self.res_list if i['op'] == 'r_DoesNotOwnRequiredApp']
            for i in redeem_list:
                level = self.key_controller.get_key_detail(i['key'])['level']
                self.key_controller.update_key(i['key'], level, i['game_id'], i['game_name'])
                self.bot_controller.update_bot_available(i['bot_name'], 'Y')
                print 'DoesNotOwnRequiredApp:{}-{}-[{}]'.format(i['bot_name'], i['game_id'], i['game_name'])

        def _owns_executor():
            own_list = [i for i in self.res_list if i['op'] == 'owns']
            bot_name_set = set()
            for i in own_list:
                bot_name_set.add(i['bot_name'])
            for bot_name in list(bot_name_set):
                self.bot_controller.update_bot_own_list(bot_name, [i for i in own_list if i['bot_name'] == bot_name])

        def _cmd_executor():
            the_list = [i for i in self.res_list if i['op'] == 'cmd']
            for i in the_list:
                print i['text']

        exe_list = [_2fa_executor, _addlicense_executor, _owns_executor, _redeem_executor, _cmd_executor]
        for exe in exe_list:
            exe()

    def generator(self, blueprint):
        self.transmitter(blueprint)
        self.connector()
        self.receiver()
        self.executor()


if __name__ == '__main__':
    cc = CoreController()
    pass
