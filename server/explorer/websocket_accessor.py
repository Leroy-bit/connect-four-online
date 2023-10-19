from base.entity import BaseEntity
from dataclasses import dataclass, asdict
from aiohttp.web import WebSocketResponse
import time
import asyncio
import typing

if typing.TYPE_CHECKING:
    from base.application import Request

TURN_TIMEOUT: int = 40
WAITING_FOR_USER_TIMEOUT: int = 45
REMATCH_TIMEOUT: int = 30

class ServerEvents:
    MAKED_TURN = 'MAKED_TURN'
    USER_JOINED = 'USER_JOINED'
    USER_DISCONNECTED = 'USER_DISCONNECTED'
    NEXT_USER = 'NEXT_USER'
    GAME_STARTED = 'GAME_STARTED'
    USER_WIN = 'USER_WIN'
    DRAW = 'DRAW'
    REMATCH_REQUEST = 'REMATCH_REQUEST'
    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'

class ClientEvents:
    DISCONNECT = 'DISCONNECT'
    MAKE_TURN = 'MAKE_TURN'
    REMATCH = 'REMATCH'

class DisconnectReasons:
    REMATCH_TIMEOUT = 'REMATCH_TIMEOUT'
    WAITING_FOR_USER_TIMEOUT = 'WAITING_FOR_USER_TIMEOUT'
    TURN_TIMEOUT = 'TURN_TIMEOUT'

@dataclass
class Event:
    '''Event dataclass.

    Attributes:
        event: Event name.
        data: Event data.
    '''
    event: str
    data: dict

    def __str__(self) -> str:
        return f'<Event:{self.event}>'

@dataclass
class Connection:
    '''Connection dataclass.
    
    Attributes:
        ws: WebSocketResponse instance.
        timeout_task: asyncio.Task instance.
        close_callback: Callback function that running on connection close.
    '''
    ws: WebSocketResponse
    timeout_task: asyncio.Task = None
    close_callback: typing.Callable = None


class WebSocketAccessor(BaseEntity):
    '''WebSocketAccessor class. Manage the websocket connections.

    Attributes:
        connections: All connections.
    '''

    connections: dict[int, dict[int, Connection]] = {}

    async def open(self, request: 'Request') -> None:
        '''Open a connection.'''
        ws = WebSocketResponse()
        await ws.prepare(request)
        game_id = request.game_id
        user_id = request.user_id
        user_name = request.user_name
        
        if (await self.explorer.game_accessor.checkIfGameExists(game_id)):
            if not (await self.explorer.game_accessor.checkIfUserInGame(game_id, user_id)) \
            and not (await self.explorer.game_accessor.checkIfUsersCountIsEnough(game_id)):
                
                self.connections[game_id][user_id] = Connection(ws)
                await self.explorer.ws.send(
                    game_id, 
                    user_id, 
                    Event(
                        ServerEvents.CONNECTED, 
                        {'users': (await self.explorer.game_accessor.getAllUsers(game_id))}
                    )
                )
                user = await self.explorer.game_accessor.addUser(game_id, user_id, user_name)
                await self.broadcast(game_id, Event(ServerEvents.USER_JOINED, asdict(user)), [user_id])
                await self.explorer.game_accessor.startGame(game_id)
        else:
            self.connections[game_id] = {user_id: Connection(ws)}
            await self.send(game_id, user_id, Event(ServerEvents.CONNECTED, {}))
            await self.explorer.game_accessor.createGame(game_id, user_id, user_name)
            await self.createWaitingForUserTimeoutTask(game_id, user_id)
        self.explorer.logger.trace(f'User {user_name}[{user_id}] openned connection on game: {game_id}')
        
    async def close(self, game_id: int, user_id: int, reason: str | None = None) -> None:
        '''Close a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        if reason:
            await self.explorer.ws.send(game_id, user_id, Event(ServerEvents.DISCONNECTED, {'reason': reason}))
        eventData = {'user_id': user_id}
        if reason:
            eventData['reason'] = reason
        await self.broadcast(game_id, Event('USER_DISCONNECTED', eventData), [user_id])
        await self._close(game_id, user_id)

    async def closeAll(self, game_id: int, reason: str | None = None) -> None:
        '''Close all connections in a game.'''
        if not self.connections.get(game_id):
            return
        if reason:
            await self.broadcast(game_id, Event(ServerEvents.DISCONNECTED, {'reason': reason}))
        for user_id in list(self.connections[game_id].keys()):
            await self._close(game_id, user_id)
    
    async def _close(self, game_id: int, user_id: int) -> None:
        '''Low level close connection.'''
        connection = self.connections.get(game_id).pop(user_id)

        if connection.close_callback:
            await connection.close_callback(user_id)

        if connection.timeout_task:
            connection.timeout_task.cancel()
        
        if not connection.ws.closed:
            await connection.ws.close()

    async def readStream(self, game_id: int, user_id: int) -> typing.AsyncIterable[Event]:
        '''Read stream from a connection. Return iterator that iterate Event instance.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return

        async for msg in self.connections[game_id][user_id].ws:
            data = msg.json()
            if 'event' in data and 'data' in data:
                yield Event(data['event'], data['data'])

    async def send(self, game_id: int, user_id: int, event: Event) -> None:
        '''Send event to a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        await self.connections[game_id][user_id].ws.send_json(asdict(event))
        self.explorer.logger.trace(f'Send {event} to {user_id} in game {game_id}')

    async def broadcast(self, game_id: int, event: Event, except_of: list[int] = []) -> None:
        '''Broadcast event to all connections in a game.'''
        if not self.connections.get(game_id):
            return
        tasks = []
        for user_id in self.connections[game_id]:
            if except_of and user_id in except_of:
                continue
            tasks.append(self.send(game_id, user_id, event))
        await asyncio.gather(*tasks)

    async def isClosed(self, game_id: int, user_id: int) -> bool:
        '''Check if connection is closed.'''
        if not self.connections.get(game_id):
            return True
        if self.connections[game_id].get(user_id):
            return False
        return self.connections[game_id][user_id].ws.closed

    async def createTurnTimeoutTask(self, game_id: int, user_id: int) -> None:
        '''Create turn timeout task for a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        await self.cancelTimeoutTask(game_id, user_id)
        self.connections[game_id][user_id].timeout_task = (await self.createTimeoutTask(
            TURN_TIMEOUT, 
            self.close, 
            game_id=game_id, 
            user_id=user_id, 
            reason=DisconnectReasons.TURN_TIMEOUT
        ))

    async def createWaitingForUserTimeoutTask(self, game_id: int, user_id: int) -> None:
        '''Create waiting for user timeout task for a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        await self.cancelTimeoutTask(game_id, user_id)
        self.connections[game_id][user_id].timeout_task = (await self.createTimeoutTask(
            WAITING_FOR_USER_TIMEOUT, 
            self.closeAll, 
            game_id=game_id,
            reason=DisconnectReasons.WAITING_FOR_USER_TIMEOUT
        ))

    async def createRematchTimeoutTask(self, game_id: int, user_id: int) -> None:
        '''Create rematch timeout task for a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        await self.cancelTimeoutTask(game_id, user_id)
        self.connections[game_id][user_id].timeout_task = (await self.createTimeoutTask(
            REMATCH_TIMEOUT, 
            self.closeAll, 
            game_id=game_id,
            reason=DisconnectReasons.REMATCH_TIMEOUT
        ))

    async def cancelTimeoutTask(self, game_id: int, user_id: int) -> None:
        '''Cancel turn timeout task for a connection.'''
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        if self.connections[game_id][user_id].timeout_task:
            self.connections[game_id][user_id].timeout_task.cancel()

    async def cancelGameTimeoutTasks(self, game_id: int) -> None:
        '''Cancel all timeout tasks in a game.'''
        if not self.connections.get(game_id):
            return
        for user_id in self.connections[game_id]:
            if self.connections[game_id][user_id].timeout_task:
                self.connections[game_id][user_id].timeout_task.cancel()

    async def createTimeoutTask(self, timeout: int, callback: typing.Callable, **kwargs) -> None:
        '''Create timeout task.'''
        def log_timeout(result: asyncio.Task):
            try:
                exc = result.exception()
            except asyncio.CancelledError:
                return

            if exc:
                self.explorer.logger.error(f'Can not close User({kwargs.get("user_id")}) in game {kwargs.get("game_id")} connection by {kwargs.get("reason")}')
                self.explorer.logger.error(exc)
            else:
                self.explorer.logger.trace(f'User({kwargs.get("user_id")}) in game {kwargs.get("game_id")} was closed by inactivity')

        task = asyncio.create_task(self._createTimeoutTask(callback, timeout, **kwargs))
        task.add_done_callback(log_timeout)
        return task

    async def _createTimeoutTask(self, callback: typing.Callable, timeout: int, **kwargs) -> None:
        '''Low level create timeout task.'''
        await asyncio.sleep(timeout)
        return await callback(**kwargs)

    


