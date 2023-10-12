from aiohttp import web
from loguru import logger
import sys
import ssl
from base.application import Application
from core.routes import setup_routes, setup_middlewares
from explorer import Explorer
import config

async def on_startup(app: Application):
    pass

def create_app() -> Application:
    app = Application()
    _logger = logger
    _logger.remove()
    _logger.add(sys.stderr, level=config.LOG_LEVEL)
    app.explorer = Explorer(app, _logger)
    app.on_startup.append(on_startup)
    app.explorer.bot_accessor.setup()
    setup_routes(app)
    setup_middlewares(app)
    _logger.info('App created')
    return app

if __name__ == '__main__':
    port = 80
    ssl_context = None
    if config.SSL_CERT and config.SSL_PRIVATE_KEY:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.load_cert_chain(config.SSL_CERT, config.SSL_PRIVATE_KEY)
        port = 443
    web.run_app(create_app(), port=port, ssl_context=ssl_context)
    