from aiohttp import web
from base.application import Request
import typing

@web.middleware
async def WebAppMiddleware(request: Request, handler: typing.Callable[[Request], typing.Awaitable[web.Response]]) -> web.Response:
        if request.path.startswith('/ws'):
            try:
                data = request.app.explorer.bot_accessor.check_user_data(request.url.query_string)
                request.user_id = data.user.id
                request.game_id = request.rel_url.query['chat_instance'] # at the time of writing this code, the chat_instance is not support by aiogram
                request.user_name = '@' + data.user.username if data.user.username else data.user.first_name
                return await handler(request)
            
            except Exception as exc:
                # return web.Response(text='wrong data from user', status=400)
                raise exc
        else:
            return await handler(request)

    