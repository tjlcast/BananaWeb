# -*- coding:utf-8 -*-

import logging

import asyncio

from banana.orm.BananaOrm import ModelMetaclass, select, execute

logging.basicConfig(level=logging.DEBUG)


# orm 的顶层类 Model
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        # 给实例装载成员
        # 重要： 实例成员
        super(Model, self).__init__(**kw)

    # 修改对实例变量的访问方式 instanceA.key => instanceA[key]
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except AttributeError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 修改对类对象成员的访问方式
    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        ' find object by primary key. '
        rs = yield from select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)


# orm 对象的字段成员变量(顶类)
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


# orm 对象的str字段成员变量
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='int'):
        super().__init__(name, ddl, primary_key, default)
