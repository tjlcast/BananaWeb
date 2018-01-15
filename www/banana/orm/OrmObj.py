# -*- coding:utf-8 -*-

from www.banana.orm.BananaOrm import ModelMetaclass


# orm 的顶层类 Model
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass

    def getValue(self, key):
        pass

    def getValueOrDefault(self, key):
        pass


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

