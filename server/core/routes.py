from aiohttp.abc import Application
from core.views import WebSocketView, MiniAppView
from core.middlewares import WebAppMiddleware
from config import BASE_DIR
import os

def setup_routes(app: Application):
    app.router.add_view('/ws', WebSocketView)
    app.router.add_static('/assets', os.path.join(BASE_DIR, 'client', 'dist', 'assets'))
    app.router.add_view('/', MiniAppView)

def setup_middlewares(app: Application):
    app.middlewares.append(WebAppMiddleware)