# coding=utf-8
import re
import json
from model.key_manager import KeyManager


class KeyController(object):
    def __init__(self):
        self.key_manager = KeyManager()

    @staticmethod
    def detection_key(keys):
        arr, temp = [], keys.strip().split()
        for each in temp:
            arr.extend(each.split(','))
        _key = [each for each in arr if re.match(r'.{5}-.{5}-.{5}', each) is not None]
        res = ','.join(_key)
        print 'key num: ', len(_key)
        print 'key    : ', res
        return _key

    def add_key_list(self, the_text, level, game_id):
        key_list = self.detection_key(the_text)
        for key in key_list:
            self.key_manager.add_key(key, level, game_id)

    def get_need_redeem_list(self):
        key_set = set()
        res_list = self.key_manager.get_level('1')
        for i in res_list:
            key_set.add(i['key'])
        for game_id in self.key_manager.get_all_game_id():
            print game_id
        return res_list

    def get_key_detail(self, key):
        return self.key_manager.get_key(key)[0]

    def update_key(self, key, level, game_id):
        return self.key_manager.update_key(key, level, game_id)

    def del_key_by_key(self, key):
        return self.key_manager.del_key(key)
