# coding=utf
import re
import json
import pyperclip
from the_project import PROJECT_DIR


class KeyManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(KeyManager, cls).__new__(cls)
        return cls._inst

    def __init__(self):
        self.database_name = '{}/model/keys.json'.format(PROJECT_DIR)
        try:
            with open(self.database_name) as f:
                self.database = json.load(f)
        except ValueError:
            self.database = dict()
        self.database.setdefault('key_logic', dict())
        self.database.setdefault('level_logic', dict())
        self.database.setdefault('game_logic', dict())

    def del_database(self):
        self.database = dict()
        with open(self.database_name, 'w+') as f:
            json.dump(self.database, f, indent=2)

    def storage_database(self):
        with open(self.database_name, 'w+') as f:
            json.dump(self.database, f, indent=2)

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

    def add_key(self, key, level, game_id):
        level, game_id = str(level), str(game_id)
        op = False
        if self.database['key_logic'].get(key) is None:
            self.database['key_logic'].setdefault(key, {'level': level, 'game_id': game_id})
            self.database['level_logic'].setdefault(level, dict())
            self.database['level_logic'][level].setdefault(key, game_id)
            self.database['game_logic'].setdefault(game_id, dict())
            self.database['game_logic'][game_id].setdefault(key, level)
            self.storage_database()
            op = True
        return op

    def del_key(self, key):
        op = False
        if self.database['key_logic'].get(key) is not None:
            self.database['game_logic'][self.database['key_logic'][key]['game_id']].pop(key)
            self.database['level_logic'][str(self.database['key_logic'][key]['level'])].pop(key)
            self.database['key_logic'].pop(key)
            self.storage_database()
            op = True
        return op

    def update_key(self, key, level, game_id):
        level, game_id = str(level), str(game_id)
        op = False
        if self.del_key(key):
            self.database['key_logic'].setdefault(key, {'level': level, 'game_id': game_id})
            self.database['level_logic'].setdefault(level, dict())
            self.database['level_logic'][level].setdefault(key, game_id)
            self.database['game_logic'].setdefault(game_id, dict())
            self.database['game_logic'][game_id].setdefault(key, level)
            self.storage_database()
            op = True
        return op

    def get_key(self, key):
        if self.database['key_logic'].get(key) is not None:
            return {'key': key, 'level': self.database['key_logic'][key]['level'],
                    'game_id': self.database['key_logic'][key]['game_id']}
        return None


if __name__ == '__main__':
    km = KeyManager()
    text = pyperclip.paste()
    text = 'TPDTZ-D7N8B-4CN3Z, J4MM3-TWTHW-0IM94, TMNMA-I64KZ-D685W, 3R67F-TFPED-0AVAV, 7I7BW-H436D-XNP5G,'
    km.del_database()
    km.add_key(text, 2, 'null')
    km.del_key('J4MM3-TWTHW-0IM94')
    km.update_key('TPDTZ-D7N8B-4CN3Z', 1, '09090')
    print km.get_key('TPDTZ-D7N8B-4CN3Z')
    pass
