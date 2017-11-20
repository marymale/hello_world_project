# coding=utf-8
import pyperclip
from controller.core_controller import CoreController


class View(object):
    def __init__(self):
        self.controller = CoreController()

    def twofa(self, bot_name, op):
        self.controller.generator('2fa {} {}'.format(bot_name, op))

    def addlicense(self, game_id):
        self.controller.generator('addlicense {}'.format(game_id))

    def update_all_owns(self):
        self.controller.generator('owns')

    def update_bot_owns(self, bot_name):
        self.controller.generator('owns {} *'.format(bot_name))

    def add_keys(self, key_text, level, game_id):
        key_text = key_text.replace('\n', ',')
        key_text = key_text.replace(' ', ',')
        self.controller.generator('addkey {} {} {}'.format(key_text, level, game_id))


if __name__ == '__main__':
    v = View()
    # v.add_keys(pyperclip.paste(), 0, 'null')
    v.twofa('marymale0', 1)
