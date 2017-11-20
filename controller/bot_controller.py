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


if __name__ == '__main__':
    owns = [{'game_id': u'209080', 'bot_name': u'marymale0', 'game_name': 'Guns of Icarus Online', 'op': 'owns'},
                {'game_id': u'31220', 'bot_name': u'marymale0', 'game_name': 'Sam & Max 301: The Penal Zone',
                 'op': 'owns'},
                {'game_id': u'31230', 'bot_name': u'marymale0', 'game_name': 'Sam & Max 302: The Tomb of Sammun-Mak',
                 'op': 'owns'},
                {'game_id': u'31240', 'bot_name': u'marymale0', 'game_name': "Sam & Max 303: They Stole Max's Brain!",
                 'op': 'owns'}, {'game_id': u'31250', 'bot_name': u'marymale0',
                                 'game_name': 'Sam & Max 304: Beyond the Alley of the Dolls', 'op': 'owns'},
                {'game_id': u'31260', 'bot_name': u'marymale0',
                 'game_name': 'Sam & Max 305: The City that Dares not Sleep', 'op': 'owns'},
                {'game_id': u'234940', 'bot_name': u'marymale0', 'game_name': 'The 39 Steps', 'op': 'owns'}]
    bc = BotController()
    bc.bot_manager.add_bot('asf',  {'owns': {}})
    bc.update_bot_own_list('asf', owns)
    print bc.bot_manager.get_bot('asf')
    bc.bot_manager.del_bot('asf')
