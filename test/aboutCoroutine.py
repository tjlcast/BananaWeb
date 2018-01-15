# -*- coding: utf-8 -*-


import threading
import asyncio


@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.current_thread())
    yield from asyncio.sleep(1)
    print('Hello world! (%s)' % threading.current_thread())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

