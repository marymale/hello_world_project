# coding=utf


class BotManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(BotManager, cls).__new__(cls)
        return cls._inst


if __name__ == '__main__':

    pass
