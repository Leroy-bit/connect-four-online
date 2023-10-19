from base.entity import BaseEntity
from explorer.websocket_accessor import Event, ClientEvents, ServerEvents

class WebSocketManager(BaseEntity):
    '''WebSocketManager class. Manage the WebSocketAccessor and GameAccessor instances.'''
    
    async def handleConnection(self, game_id: int, user_id: int) -> None:
        '''Handle a connection.'''
        async for event in self.explorer.ws.readStream(game_id, user_id):
            self.explorer.logger.trace(f'Received {event} from {user_id} in game {game_id}')
            if event.event == ClientEvents.MAKE_TURN:
                await self.explorer.game_accessor.makeTurn(game_id, user_id, event.data.get('column'))
            elif event.event == ClientEvents.REMATCH:
                await self.explorer.game_accessor.rematch(game_id, user_id)
            elif event == ClientEvents.DISCONNECT:
                await self.handleDisconnect(game_id, user_id)
    
    async def handleDisconnect(self, game_id: int, user_id: int) -> None:
        '''Do some things when a user disconnects.'''
        if not (await self.explorer.ws.isClosed(game_id, user_id)):
            await self.explorer.ws.broadcast(
                game_id, 
                Event(ServerEvents.USER_DISCONNECTED, {'user_id': user_id}), 
                [user_id]
            )
        await self.explorer.game_accessor.closeGame(game_id)
        self.explorer.logger.trace(f'User {user_id} disconnected from game {game_id}')
    