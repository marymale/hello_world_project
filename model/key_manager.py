# coding=utf
import json
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
        self.database.setdefault('key_logic', dict())
        self.database.setdefault('level_logic', dict())
        self.database.setdefault('game_logic', dict())
        with open(self.database_name, 'w+') as f:
            json.dump(self.database, f, indent=2)

    def storage_database(self):
        with open(self.database_name, 'w+') as f:
            json.dump(self.database, f, indent=2)

    def add_key(self, key, level, game_id, game_name):
        level, game_id = str(level), str(game_id)
        op = False
        if self.database['key_logic'].get(key) is None:
            self.database['key_logic'].setdefault(key, {'level': level, 'game_id': game_id, 'game_name': game_name})
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

    def update_key(self, key, level, game_id, game_name):
        level, game_id = str(level), str(game_id)
        op = False
        if self.del_key(key):
            if self.add_key(key, level, game_id, game_name):
                op = True
        return op

    def get_key(self, key):
        if self.database['key_logic'].get(key) is not None:
            return [{'key': key, 'level': self.database['key_logic'][key]['level'],
                    'game_id': self.database['key_logic'][key]['game_id']}]
        return []

    def get_level(self, level):
        level = str(level)
        if self.database['level_logic'].get(level) is not None:
            return [{'key': i, 'level': level, 'game_id': self.database['level_logic'][level][i]} for i in
                    self.database['level_logic'][level].keys()]
        return []

    def get_game_id(self, game_id):
        game_id = str(game_id)
        if self.database['game_logic'].get(game_id) is not None:
            return [{'key': i, 'level': self.database['game_logic'][game_id][i], 'game_id': game_id} for i in
                    self.database['game_logic'][game_id].keys()]
        return []

    def get_all_game_id(self):
        return self.database['game_logic'].keys()
