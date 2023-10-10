from base.entity import BaseEntity
from dataclasses import dataclass, asdict
from aiohttp.web import WebSocketResponse
import time
import asyncio
import typing

if typing.TYPE_CHECKING:
    from base.application import Request
    from explorer.game_accessor import TURN_TIMEOUT

@dataclass
class Event:
    event: str
    data: dict

    def __str__(self) -> str:
        return f'<Event:{self.event}>'

@dataclass
class Connection:
    ws: WebSocketResponse
    last_response: float
    turn_timeout_task: asyncio.Task = None
    close_callback: typing.Callable = None


class WebSocketAccessor(BaseEntity):

    connections: dict[int, dict[int, Connection]] = {}

    async def open(self, request: 'Request') -> None:
        ws = WebSocketResponse()
        await ws.prepare(request)
        print(self.explorer.game_accessor.GAMES)
        if request.game_id in self.explorer.game_accessor.GAMES:
            if request.user_id not in self.explorer.game_accessor.GAMES[request.game_id].players & len(self.explorer.game_accessor.GAMES[request.game_id].players) < 2:
                print('game exists')
                self.connections[request.game_id][request.user_id] = Connection(ws, time.time())
                await self.explorer.ws.send(request.game_id, request.user_id, Event('CONNECT', {'players': (await self.explorer.game_accessor.getAllPlayers(request.game_id))}))
                await self.explorer.game_accessor.addPlayer(request.game_id, request.user_id, request.user_name)
        else:
            print('game not exists')
            self.connections[request.game_id] = {request.user_id: Connection(ws, time.time())}
            await self.explorer.ws.send(request.game_id, request.user_id, Event('CONNECT', {}))
            await self.explorer.game_accessor.createGame(request.game_id, request.user_id, request.user_name)
        print(f'Player {request.user_name}[{request.user_id}] connected to game {request.game_id}')
        


    async def close(self, game_id, player_id) -> None:
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(player_id):
            return
        await self.broadcast(game_id, Event('PLAYER_DISCONNECTED', {'player_id': player_id}), [player_id])
        await self._close(game_id, player_id)

    async def close_all(self, game_id) -> None:
        if not self.connections.get(game_id):
            return
        for player_id in list(self.connections[game_id]):
            await self._close(game_id, player_id)
    
    async def _close(self, game_id, player_id) -> None:
        connection = self.connections.get(game_id).pop(player_id)

        if connection.close_callback:
            await connection.close_callback(player_id)
        
        if not connection.ws.closed:
            await connection.ws.close()

    async def read_stream(self, game_id, player_id) -> typing.AsyncIterable[Event]:
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(player_id):
            return

        async for msg in self.connections[game_id][player_id].ws:
            await self.refresh_connection(game_id, player_id)
            data = msg.json()
            print(data)
            if 'event' in data and 'data' in data:
                yield Event(data['event'], data['data'])

    async def send(self, game_id: int, user_id: int, event: Event) -> None:
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(user_id):
            return
        await self.connections[game_id][user_id].ws.send_json(asdict(event))
        print(f'Send {event} to {user_id} in game {game_id}')

    async def broadcast(self, game_id: int, event: Event, except_of: list[int] = []) -> None:
        if not self.connections.get(game_id):
            return
        tasks = []
        for user_id in self.connections[game_id]:
            if except_of and user_id in except_of:
                continue
            tasks.append(self.send(game_id, user_id, event))
        await asyncio.gather(*tasks)

    async def create_turn_timeout_task(self, game_id: int, player_id: int) -> None:
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(player_id):
            return
        self.connections[game_id][player_id].turn_timeout_task = await self._create_turn_timeout_task(game_id, player_id, TURN_TIMEOUT, self.close)

    async def cancel_turn_timeout_task(self, game_id: int, player_id: int) -> None:
        if not self.connections.get(game_id):
            return
        if not self.connections[game_id].get(player_id):
            return
        if self.connections[game_id][player_id].turn_timeout_task:
            self.connections[game_id][player_id].turn_timeout_task.cancel()

    async def _create_turn_timeout_task(self, game_id: int, player_id: int, timeout: int, callback: typing.Callable) -> None:
        def log_timeout(result: asyncio.Task):
            try:
                exc = result.exception()
            except asyncio.CancelledError:
                return

            if exc:
                print(f'!!!Can not close Player({player_id}) in game {game_id} connection by timeout\n')
            else:
                self.logger.info(f'!!!Player({player_id}) in game {game_id} was closed by inactivity')

        task = asyncio.create_task(self._create_timeout_task(self.close, TURN_TIMEOUT, [game_id, player_id]))
        task.add_done_callback(log_timeout)
        return task

    async def _create_timeout_task(callback: typing.Callable, timeout: int, args: list) -> None:
                await asyncio.sleep(timeout)
                return await callback(*args)
    
    async def refresh_connection(self, game_id, player_id) -> None:
        self.connections[game_id][player_id].last_response = time.time()

    


