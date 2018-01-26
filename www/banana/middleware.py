# -*- utf-8 -*-

import asyncio
import logging

from aiohttp import web

logging.basicConfig(level=logging.INFO)


@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        # 记录日志
        logging.info('Request: %s %s ' % (request.method, request.path))
        # 继续处理请求
        return (yield from handler(request))
    return logger


@asyncio.coroutine
def response_factory(app, handler):
    def response(request):
        # result
        r = yield from handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = "application/octet-stream"
            return resp
        if isinstance(r, str):
            resp = web.Response(body = r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp

