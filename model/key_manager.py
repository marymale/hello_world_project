# coding=utf
import re
import json
import pyperclip
from the_project import PROJECT_DIR


class KeyManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(KeyManager, cls).__new__(cls)
        try:
            with open('{}/model/keys.json'.format(PROJECT_DIR)) as f:
                cls.database = json.load(f)
        except ValueError:
            cls.database = dict()
        return cls._inst

    @staticmethod
    def detection_key(keys):
        arr, temp = [], keys.strip().split()
        for each in temp:
            arr.extend(each.split(','))
        _key = [each for each in arr if re.match(r'.....-.....-.....', each) is not None]
        res = ','.join(_key)
        print 'key num: ', len(_key)
        print 'key    : ', res
        return _key

    def storage_database(self):
        with open('{}/model/keys.json'.format(PROJECT_DIR), 'w+') as f:
            json.dump(self.database, f, indent=2)

    def add_key(self, the_text, level, game_id):
        level, game_id = str(level), str(game_id)
        self.database.setdefault('key_logic', dict())
        self.database.setdefault('level_logic', dict())
        self.database.setdefault('game_logic', dict())
        key_list = self.detection_key(the_text)
        for k in key_list:
            if self.database['key_logic'].get(k) is None:
                self.database['key_logic'].setdefault(k, {'level': level, 'game_id': game_id})
                self.database['level_logic'].setdefault(level, dict())
                self.database['level_logic'][level].setdefault(k, game_id)
                self.database['game_logic'].setdefault(game_id, dict())
                self.database['game_logic'][game_id].setdefault(k, level)
        self.storage_database()

    def change_key(self, key, level, game_id):
        level, game_id = str(level), str(game_id)
        if self.database['key_logic'].get(key) is not None:
            self.database['game_logic'][self.database['key_logic'][key]['game_id']].pop(key)
            self.database['level_logic'][str(self.database['key_logic'][key]['level'])].pop(key)
            self.database['key_logic'].pop(key)

            self.database['key_logic'].setdefault(key, {'level': level, 'game_id': game_id})
            self.database['level_logic'].setdefault(level, dict())
            self.database['level_logic'][level].setdefault(key, game_id)
            self.database['game_logic'].setdefault(game_id, dict())
            self.database['game_logic'][game_id].setdefault(key, level)

            self.storage_database()
            return True
        return False


if __name__ == '__main__':
    km = KeyManager()
    text = pyperclip.paste()
    km.add_key(text, 2, 'null')
    km.change_key('TPDTZ-D7N8B-4CN3Z', 1, '09090')
    pass
