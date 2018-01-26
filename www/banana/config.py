# -*- coding:utf-8 -*-

from www.banana import config_default


class Dict(dict):
    '''
    sample dict and support access as x,y.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(default, override):
    new_dict = {}
    for k, v in default.items():
        if k in override:
            if isinstance(v, dict):
                new_dict[k] = merge(v, override[k])
            else:
                new_dict[k] = override[k]
        else:
            new_dict[k] = v
    return new_dict


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


# =============== 执行代码
configs = config_default.configs

try:
    import wwww.banana.config_override
    configs = merge(configs, wwww.banana.config_override.configs)
except ImportError:
    pass

configs = toDict(configs)