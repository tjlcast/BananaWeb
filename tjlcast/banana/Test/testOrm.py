# -*- coding:utf-8 -*-

import asyncio

from banana.orm.BananaOrm import create_pool
from banana.orm.OrmObj import Model, StringField, IntegerField


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

    loop.run_until_complete(asyncio.wait(create_pool(loop, ), user.save()))
    loop.close()



