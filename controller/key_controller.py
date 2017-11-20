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

if __name__ == '__main__':
    kc = KeyController()
    text = 'TPDTZ-D7N8B-4CN3Z, J4MM3-TWTHW-0IM94, TMNMA-I64KZ-D685W, 3R67F-TFPED-0AVAV, 7I7BW-H436D-XNP5G,'
    kc.key_manager.del_database()
    kc.add_key_list(text, 2, 'null')
    kc.key_manager.del_key('J4MM3-TWTHW-0IM94')
    kc.key_manager.update_key('TPDTZ-D7N8B-4CN3Z', 1, '09090')
    print kc.key_manager.get_key('TPDTZ-D7N8B-4CN3Z')
    print kc.key_manager.get_level(2)
    print kc.key_manager.get_game_id('09090')
    pass
