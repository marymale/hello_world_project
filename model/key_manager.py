# coding=utf


class KeyManager(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(KeyManager, cls).__new__(cls)
        return cls._inst


if __name__ == '__main__':

    pass
