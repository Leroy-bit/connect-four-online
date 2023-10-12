from base.application import Application
from core.views import WebSocketView, MiniAppView
from core.middlewares import WebAppMiddleware
from config import BASE_DIR
import os

def setup_routes(app: Application):
    app.explorer.logger.debug('Setting up routes')
    app.router.add_view('/ws', WebSocketView)
    app.router.add_static('/assets', os.path.join(BASE_DIR, 'client', 'dist', 'assets'))
    app.router.add_view('/', MiniAppView)

def setup_middlewares(app: Application):
    app.explorer.logger.debug('Setting up middlewares')
    app.middlewares.append(WebAppMiddleware)