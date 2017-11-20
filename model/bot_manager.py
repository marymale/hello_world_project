# coding=utf-8
import json
from the_project import PROJECT_DIR


class BotManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(BotManager, cls).__new__(cls)
        return cls._inst

    def __init__(self):
        self.database_name = '{}/model/bots.json'.format(PROJECT_DIR)
        try:
            with open(self.database_name) as f:
                self.database = json.load(f)
        except ValueError:
            self.database = dict()

    def storage_database(self):
        with open(self.database_name, 'w+') as f:
            json.dump(self.database, f, indent=2)

    def add_bot(self, bot_name, bot_dict):
        op = False
        if self.database.get(bot_name) is None:
            self.database.setdefault(bot_name, bot_dict)
            self.storage_database()
            op = True
        return op

    def del_bot(self, bot_name):
        op = False
        if self.database.get(bot_name) is not None:
            self.database.pop(bot_name)
            self.storage_database()
            op = True
        return op

    def update_bot(self, bot_name, bot_dict):
        op = False
        if self.del_bot(bot_name):
            if self.add_bot(bot_name, bot_dict):
                op = True
        return op

    def get_bot(self, bot_name):
        if self.database.get(bot_name) is not None:
            return self.database[bot_name]
        return None

    def get_all_bot_names(self):
        return self.database.keys()


if __name__ == '__main__':
    bm = BotManager()
    bm.add_bot('asd', {'a': "k"})
    print bm.get_bot('asd')
    bm.update_bot('asd', {'a': 'asd'})
    print bm.get_bot('asd')
    bm.del_bot('asd')
    print bm.get_bot('asd')
    print bm.get_all_bot_names()
