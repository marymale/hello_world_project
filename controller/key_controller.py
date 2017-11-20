# coding=utf-8
import re
import json
import requests
import urllib
from the_project import PROJECT_DIR
from model.key_manager import KeyManager
from model.bot_manager import BotManager


class CoreController(object):
    def __init__(self):
        self.key_manager = KeyManager()

    @staticmethod
    def detection_key(keys):
        arr, temp = [], keys.strip().split()
        for each in temp:
            arr.extend(each.split(','))
        _key = [each for each in arr if re.match(r'.{5}-.{5}-.{5}', each) is not None]
        res = ','.join(_key)
        print 'key num: ', len(_key)
        print 'key    : ', res
        return _key

    def add_key_list(self, text):
