import typing
from explorer.game_accessor import GameAccessor
from explorer.websocket_manager import WebSocketManager
from explorer.websocket_accessor import WebSocketAccessor
from explorer.db import DBAccessor
from explorer.bot import BotAccessor
from loguru._logger import Logger

if typing.TYPE_CHECKING:
    from base.application import Application

class Explorer:
    '''
    Explorer is a class that provides access to all the components of the application from any place in program.
    
    Attributes:
        app: Application instance.
        game_accessor: GameAccessor instance.
        ws: WebSocketAccessor instance.
        ws_manager: WebSocketManager instance.
        bot_accessor: BotAccessor instance.
        logger: Logger instance.

    Initialization arguments:
        app: Application instance.
        logger: Logger instance.
    '''
    def __init__(self, app: 'Application', logger: Logger):
        self.app = app
        self.game_accessor: GameAccessor = GameAccessor(self)
        self.ws: WebSocketAccessor = WebSocketAccessor(self)
        self.ws_manager: WebSocketManager = WebSocketManager(self)
        self.bot_accessor: BotAccessor = BotAccessor(self)
        self.logger: Logger = logger
        self.db: DBAccessor = DBAccessor(self)