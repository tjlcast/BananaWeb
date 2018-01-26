# -*- coding: utf-8 -*-

import logging
import asyncio, os, json, time
from aiohttp import web

from www.banana.coroweb import add_routes
from www.banana.middleware import response_factory, logger_factory

logging.basicConfig(level=logging.INFO)


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])
    # app.router.add_route('GET', '/', index)
    add_routes(app, 'handler')
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
