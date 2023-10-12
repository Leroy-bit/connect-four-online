import typing
from explorer.game_accessor import GameAccessor
from explorer.websocket_manager import WebSocketManager
from explorer.websocket_accessor import WebSocketAccessor
from explorer.bot import BotAccessor
from loguru._logger import Logger

if typing.TYPE_CHECKING:
    from base.application import Application

class Explorer:
    def __init__(self, app: 'Application', logger: Logger):
        self.app = app
        self.game_accessor: GameAccessor = GameAccessor(self)
        self.ws: WebSocketAccessor = WebSocketAccessor(self)
        self.ws_manager: WebSocketManager = WebSocketManager(self)
        self.bot_accessor: BotAccessor = BotAccessor(self)
        self.logger: Logger = logger