# coding=utf-8
import datetime
from the_project import TIME_FMT
from model.bot_manager import BotManager


class BotController(object):
    def __init__(self):
        self.bot_manager = BotManager()

    def update_bot_own_list(self, bot_name, own_list):
        bot_dict = self.bot_manager.get_bot(bot_name)
        op = False
        if bot_dict is not None:
            bot_dict.pop('owns')
            bot_dict.setdefault('owns', {i['game_id']: i['game_name'] for i in own_list})
            if self.bot_manager.update_bot(bot_name, bot_dict):
                op = True
        return op

    def get_all_bot_names(self):
        return self.bot_manager.get_all_bot_names()

    def add_bot_own(self, bot_name, game_id, game_name):
        bot_dict = self.bot_manager.get_bot(bot_name)
        bot_dict.setdefault('owns', dict())
        bot_dict['owns'].setdefault(game_id, game_name)
        return self.bot_manager.update_bot(bot_name, bot_dict)

    def update_bot_available(self, bot_name, state):
        bot_dict = self.bot_manager.get_bot(bot_name)
        bot_dict.setdefault('state', state)
        bot_dict['state'] = state
        bot_dict.setdefault('last_time', datetime.datetime.now().strftime(TIME_FMT))
        bot_dict['last_time'] = datetime.datetime.now().strftime(TIME_FMT)
        return self.bot_manager.update_bot(bot_name, bot_dict)

    def get_bot_needs(self, game_id):
        res_list = []
        for bot in self.get_all_bot_names():
            if self.bot_manager.get_bot(bot)['owns'].get(game_id) is None:
                res_list.append(bot)
        return res_list
if __name__ == '__main__':
    bc = BotController()
    pass
