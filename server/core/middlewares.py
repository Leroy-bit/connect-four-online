from aiohttp import web
from base.application import Request
import typing

@web.middleware
async def WebAppMiddleware(request: Request, handler: typing.Callable[[Request], typing.Awaitable[web.Response]]) -> web.Response:
        if request.path.startswith('/ws'):
            try:
                data = (await request.app.explorer.bot_accessor.checkUserData(request.url.query_string))
                await request.app.explorer.db.handleUser(
                    data.user.id,
                    data.user.first_name,
                    data.user.last_name,
                    data.user.username,
                    data.user.language_code,
                    is_connection=True)
                
                request.user_id = data.user.id
                request.game_id = request.rel_url.query['chat_instance'] # at the time of writing this code, the chat_instance is not supported variable by aiogram
                request.user_name = '@' + data.user.username if data.user.username else data.user.first_name
                return await handler(request)
            except Exception as exc:
                return web.Response(text='wrong data from user', status=400)
        else:
            return await handler(request)

    