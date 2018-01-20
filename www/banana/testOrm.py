# -*- coding:utf-8 -*-

import asyncio

import sys;

from www.banana.orm import Model, IntegerField, StringField, create_pool

sys.path.append('/Users/tangjialiang/PycharmProjects/BananaWeb/tjlcast/banana')


class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()


if __name__ == '__main__':
    dbConfig = {
        'user': 'root',
        'password': 'destination',
        'db': 'bananaWeb',
    }
    loop = asyncio.get_event_loop()

    user = User(id=123, name='Michead')

    # loop.run_until_complete(asyncio.wait(create_pool(loop, **dbConfig)))
    loop.run_until_complete(asyncio.wait(user.save()))
    loop.close()



