# -*- coding:utf-8 -*-

import asyncio
import aiomysql

from www.banana.orm import Model, IntegerField, StringField, create_pool, destory_pool


class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()


@asyncio.coroutine
def test(loop):
        kw = {
            'user': 'root',
            'password': 'destination',
            'db': 'bananaWeb',
        }
        __pool = yield from aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('host', 3306),
            user=kw['user'],
            password=kw['password'],
            db=kw['db'],
            charset=kw.get("charset", "utf8"),
            autocommit=kw.get('autocommit', True),
            maxsize=kw.get('maxsize', 10),
            minsize=kw.get('minsize', 1),
            loop=loop
        )
        # user = User(id=123, name='Michead')
        # yield from user.save()
        global __pool
        with (yield from __pool) as conn:
            cur = yield from conn.cursor(aiomysql.DictCursor)
            yield from cur.execute("select `id`,  `name` from `users`", ())
            rs = yield from cur.fetchall()

        # users = yield from User.findAll()
        yield from destory_pool()
        pass


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
