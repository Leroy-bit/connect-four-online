from aiohttp import web
from base.application import View, Request
from config import BASE_DIR
import os

class MiniAppView(View):
    async def get(self):
        with open(os.path.join(BASE_DIR, 'client', 'dist', 'index.html'), 'r') as f:
            file = f.read()

        return web.Response(
            body=file,
            headers={
                'Content-Type': 'text/html',
            }
        )

class WebSocketView(View):
    async def get(self):
        await self.explorer.ws.open(self.request)
        print(self.request.game_id, self.request.user_id)
        print(f'Player {self.request.user_id} connected to game {self.request.game_id}')
        await self.explorer.ws_manager.handle_connection(self.request.game_id, self.request.user_id)
        await self.explorer.ws_manager.on_user_disconnect(self.request.game_id, self.request.user_id)
        # return self.explorer.ws.connections[self.request.game_id][self.request.user_id].ws