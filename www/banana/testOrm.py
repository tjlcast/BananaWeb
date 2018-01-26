# -*- coding:utf-8 -*-

import asyncio

from www.banana.orm import Model, IntegerField, StringField, create_pool, destory_pool


class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()


@asyncio.coroutine
def test(loop):
        dbConfig = {
            'user': 'root',
            'password': 'destination',
            'db': 'bananaWeb',
        }
        yield from create_pool(loop = loop, **dbConfig)
        user = User(id=123, name='Michead')
        yield from user.save()
        yield from destory_pool()


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
