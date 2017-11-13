# coding=utf-8
import json
from the_project import PROJECT_DIR


class BotManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(BotManager, cls).__new__(cls)
            with open('{}/model/bots.json'.format(PROJECT_DIR)) as f:
                cls.conf = json.load(f)
        return cls._inst

    def get_all_bot_name(self):
        return self.conf.keys()

if __name__ == '__main__':

    pass
