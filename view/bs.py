# coding=utf-8
import re
from bs4 import BeautifulSoup


def get_daily_indie_game_discounts():
    with open('Daily.html') as f:
        soup = BeautifulSoup(f, "lxml")

    game_tables = BeautifulSoup(str(soup.find_all('table', id='TableKeys')), "lxml")
    discount_list = re.findall(r"<td class=\"DIG3_14_Orange\">(.*?)\+ keys</td>", str(game_tables))
    print discount_list
    game_detail_list = game_tables.find_all(onmouseover="this.bgColor='#222222';this.style.cursor='pointer';")

    res_list = []
    for game in game_detail_list:
        game = str(game)
        list_id = re.findall(r"<td class=\"DIG3_14_Gray\" valign=\"top\">(.*?)<input class=\"DIGEasyBuy_checkbox\" data-id=\".*\" data-price=\".*\" type=\"checkbox\"/></td>", game)
        game_id = re.findall(r"<a href=\"http://store.steampowered.com/app/(.*?)/\" target=\"_blank\">", game)
        have_card = True if re.findall(r"<td valign=\"top\"><span class=\"DIG2-TitleOrange2\">(.*?)</span></td>", game) else False
        discount = [int(i.strip().split(' Points')[0]) if i.strip() != '' else 0 for i in re.findall(r"<td class=\"DIG3_14_Gray\" valign=\"top\">\\n(.*?)</td>", game)]
        buy_href = 'http://www.dailyindiegame.com/{}'.format(re.findall(r"<td valign=\"top\"><a href=\"(account_buy_.*\.html?)\"><img src=\"dig2-images/digaccount-button-buygame.png\"/></a></td>", game)[0])
        res_list.append([int(list_id[0]), game_id[0], have_card, discount, buy_href])
    return res_list, discount_list
