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

    def add_bot(self):
        pass

    def update_bot(self):
        pass

    def get_bot(self):
        pass

    def get_all_bot_name(self):
        return self.database.keys()


if __name__ == '__main__':
    bm = BotManager()
    bm.storage_database()
    print bm.get_all_bot_name()
