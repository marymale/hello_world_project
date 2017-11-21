# coding=utf-8
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
        bot_dict['owns'].setdefault(game_id, game_name)
        return self.bot_manager.update_bot(bot_name, bot_dict)
