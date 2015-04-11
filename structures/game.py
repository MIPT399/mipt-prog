from abc import ABCMeta, abstractmethod
from json import loads, dumps

__all__ = ['Point', 'Unit', 'Player', 'Action', 'Response']

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

Point = Unit = Player = Action = Response = AttrDict
