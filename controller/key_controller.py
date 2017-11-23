# coding=utf-8
import re
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
        game_id = self.key_manager.get_all_game_id()
        temp_list = [self.key_manager.get_game_id(i) for i in game_id]
        res_list = []
        for i in temp_list:
            level_set = set()
            for j in i:
                level_set.add(j['level'])
            for level in list(level_set):
                res_list.append([j for j in i if j['level'] == level])
        return res_list

    def get_key_detail(self, key):
        return self.key_manager.get_key(key)[0]

    def get_all_game_id(self):
        return self.key_manager.get_all_game_id()

    def update_key(self, key, level, game_id, game_name):
        return self.key_manager.update_key(key, level, game_id, game_name)

    def del_key_by_key(self, key):
        return self.key_manager.del_key(key)

if __name__ == '__main__':
    kc = KeyController()
    # kc.update_key('F3HJN-Q2EMA-M6LE9', 1, 34286)
    pass
