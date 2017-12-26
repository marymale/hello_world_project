# coding=utf-8
import time
import pyperclip
from controller.core_controller import CoreController


class View(object):
    def __init__(self):
        self.controller = CoreController()

    def twofa(self, bot_name, op):
        self.controller.generator('2fa {} {}'.format(bot_name, op))

    def addlicense(self, game_id):
        self.controller.generator('addlicense {}'.format(game_id))

    def cmd(self, command):
        self.controller.generator('cmd {}'.format(command))

    def del_by_id(self, game_id):
        self.controller.generator('del {}'.format(game_id))

    def update_all_owns(self):
        self.controller.generator('owns')

    def update_bot_owns(self, bot_name):
        self.controller.generator('owns {} *'.format(bot_name))

    def add_keys(self, key_text, level, game_id='null', game_name='null'):
        key_text = key_text.replace('\n', ',')
        key_text = key_text.replace(' ', ',')
        self.controller.generator('addkey {} {} {} {}'.format(key_text, level, game_id, game_name))

    def advance_redeem(self):
        self.controller.generator('redeem')

    def game_needs(self, game_id):
        self.controller.generator('need {}'.format(game_id))

    def restart(self, bot_id):
        self.controller.generator('restart {}'.format(bot_id))

    def loot_all(self):
        self.controller.generator('loot')

    def detect_daily_indie_game_discounts(self):
        from bs import get_daily_indie_game_discounts
        res_list, discount_list = get_daily_indie_game_discounts()
        res_list = [i for i in res_list if i['have_card'] and sum(i['discount']) > 0]
        buy_list = []
        for res in res_list:
            game_need = len(self.controller.bot_controller.get_bot_needs('game_id', res['game_id']))
            if game_need > 0:
                dis1 = [discount_list[i] * res['discount'][i] * 1.0 / min(discount_list[i], game_need) for i in range(len(discount_list))]
                dis1 = min([i for i in dis1 if i > 0])
                dis2 = min([float(i) for i in res['discount'] if i > 0])
                if min(dis1, dis2) < 5:
                    buy_list.append([dis1, dis2, discount_list[res['discount'].index(dis2)], res['buy_href']])
                    print
        # print res_list


if __name__ == '__main__':
    v = View()
    v.cmd('version')

    # v.del_by_id(134099)
    # v.update_all_owns()
    # v.restart('marymale')

    # while True:
    #     v.twofa('marysctggmale', 1)
    #     v.twofa('marymalesctgg', 1)
    #     v.twofa('marysctggmale', 2)
    #     v.twofa('marymalesctgg', 2)
    #     time.sleep(200)

    # v.game_needs('4000')
    v.detect_daily_indie_game_discounts()
    # v.addlicense('153186')
    # v.loot_all()

    # v.add_keys(pyperclip.paste(), 2)
    # for i in range(10):
    #     v.advance_redeem()
    #     if not v.controller.res_list:
    #         break

    pass
