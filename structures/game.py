from abc import ABCMeta, abstractmethod
from json import loads, dumps

__all__ = ['Point', 'Unit', 'Player', 'Action', 'Response', 'load', 'AttrDict']


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

Point = Unit = Player = Action = Response = AttrDict

def type_assert(o, exp_type='Action'):
    ops = {
        'Action': {'owner': str, 'id': str, 'position': 'Point'},
        'Point': {'x': int, 'y': int},
    }
    if isinstance(exp_type, str):
        type_assert(o, ops[exp_type])
    elif isinstance(exp_type, list):
        exp_type, = exp_type
        for val in o:
            type_assert(val, exp_type)
    elif isinstance(exp_type, dict):
        assert isinstance(o, dict)
        for key, val in exp_type.items():
            assert key in o
            type_assert(o[key], val)
    else:
        assert isinstance(o, exp_type)

def load(source, method_name):
    types = {
        'moveUnit': 'Action',
        'attack': 'Action',
        'getField': None,
        'wait': None
    }
    assert len(source) < 300
    if types[method_name] is None:
        return ''
    res = loads(source, object_hook=AttrDict)
    type_assert(res, types[method_name])
    return res
