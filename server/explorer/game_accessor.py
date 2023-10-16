import random
from base.entity import BaseEntity
from explorer.websocket_accessor import Event
from explorer.websocket_manager import ServerEvents
from dataclasses import dataclass, asdict

@dataclass
class Player:
    '''Player class.
    
    Attributes:
        id: Player ID.
        name: Player name.
    '''
    id: int 
    name: str

class Game:
    '''Game class.

    Attributes:
        id: Game ID.
        started: Game started.
        players: Players in game.
        board: Game board.
        boardRows: Number of rows in game board.
        boardColumns: Number of columns in game board.
        current_player_id: Current player ID.
    '''

    def __init__(self, id: int, player_id: int, user_name) -> None:
        self.id: int = id
        self.started: bool = False
        self.players: dict[int, Player] = {player_id: Player(player_id,  user_name)}
        self.rematch: bool = False
        self.board: list[list] = []
        self.boardRows: int = 7
        self.boardColumns: int = 8
        self.current_player_id: int = None


class GameAccessor(BaseEntity):
    '''GameAccessor class. Manage the game logic.

    Attributes:
        GAMES: All games.
    '''


    GAMES: dict[int, Game] = {}
    
    async def checkIfGameExists(self, game_id: int) -> bool:
        '''Checks if a game exists. Returns True if game exists.'''
        return game_id in self.GAMES
    
    async def checkIfGameStarted(self, game_id: int) -> bool:
        '''Checks if a game has started. Returns True if game has started.'''
        return self.GAMES[game_id].started
    
    async def checkIfPlayerIsCurrent(self, game_id: int, player_id: int) -> bool:
        '''Checks if a player is the current player. Returns True if player is the current player.'''
        return self.GAMES[game_id].current_player_id == player_id
    
    async def checkIfPlayerInGame(self, game_id: int, player_id: int) -> bool:
        '''Checks if a player is in a game. Returns True if player is in game.'''
        return player_id in self.GAMES[game_id].players.keys()
    
    async def checkIfPlayersCountIsEnough(self, game_id: int) -> bool:
        '''Checks if there are enough players in a game. Returns True if there are enough players.'''
        return len(self.GAMES[game_id].players) >= 2

    async def createGame(self, game_id: int, player_id: int, user_name: str) -> None:
        '''Create a new game.'''
        game = Game(game_id, player_id, user_name)
        self.GAMES[game.id] = game
        self.explorer.logger.trace(f'Game {game_id} created by {user_name}[{player_id}]')

    async def getAllPlayers(self, game_id: int) -> list[Player]:
        '''Returns all players in a game.'''
        return [asdict(player) for player in self.GAMES[game_id].players.values()]

    async def startGame(self, game_id: int) -> None:
        '''Starts a game.'''
        self.GAMES[game_id].started = True
        self.GAMES[game_id].board = []
        for _ in range(self.GAMES[game_id].boardColumns):
            self.GAMES[game_id].board.append([])
        self.GAMES[game_id].current_player_id = random.choice(list(self.GAMES[game_id].players.keys()))
        await self.explorer.ws.cancel_game_timeout_tasks(game_id)
        await self.explorer.ws.create_turn_timeout_task(game_id, self.GAMES[game_id].current_player_id)
        await self.explorer.ws.broadcast(
            game_id, 
            Event(ServerEvents.GAME_STARTED, {'current_player_id': self.GAMES[game_id].current_player_id})
        )

    async def addPlayer(self, game_id: int, player_id: int, user_name: str) -> Player:
        '''Adds a player to a game.'''
        player = Player(player_id, user_name)
        self.GAMES[game_id].players[player_id] = player
        return player
            
    
    async def checkWin(self, board: list[list[int]], columns: int, rows: int) -> int:
        '''Checks the board for a winning combination.'''
        # Check for horizontal win
        for row in range(rows):
            for column in range(columns - 3):
                if len(board[column]) > row \
                and len(board[column + 1]) > row \
                and len(board[column + 2]) > row \
                and len(board[column + 3]) > row:

                    if board[column][row] == \
                    board[column + 1][row] == \
                    board[column + 2][row] == \
                    board[column + 3][row]:

                        return board[column][row]
        
        # Check for vertical win
        for column in range(columns):
            for row in range(rows - 3):
                if len(board[column]) > row + 3:
                    if board[column][row] == \
                    board[column][row + 1] == \
                    board[column][row + 2] == \
                    board[column][row + 3]:
                        return board[column][row]
                
        # Check for positive diagonal win
        for column in range(columns - 3):
            for row in range(rows - 3):
                if len(board[column]) > row \
                and len(board[column + 1]) > row + 1 \
                and len(board[column + 2]) > row + 2 \
                and len(board[column + 3]) > row + 3:
                    
                    if board[column][row] == \
                    board[column + 1][row + 1] == \
                    board[column + 2][row + 2] == \
                    board[column + 3][row + 3]:
                        return board[column][row]
                    
        # Check for negative diagonal win
        for column in range(columns - 3):
            for row in range(3, rows):
                if len(board[column]) > row \
                and len(board[column + 1]) > row - 1 \
                and len(board[column + 2]) > row - 2 \
                and len(board[column + 3]) > row - 3:
                    
                    if board[column][row] == \
                    board[column + 1][row - 1] == \
                    board[column + 2][row - 2] == \
                    board[column + 3][row - 3]:
                        return board[column][row]
        
        return False

    async def nextPlayer(self, game_id: int) -> None:
        players_ids = list(self.GAMES[game_id].players.keys())
        next_player_id = players_ids[players_ids.index(self.GAMES[game_id].current_player_id) - 1]
        self.GAMES[game_id].current_player_id = next_player_id
        await self.explorer.ws.create_turn_timeout_task(game_id, next_player_id)
        await self.explorer.ws.broadcast(
            game_id, 
            Event(ServerEvents.NEXT_PLAYER, {'current_player_id': next_player_id})
        )

    async def makeTurn(self, game_id: int, player_id: int, column: int = None) -> None:
        '''Makes a turn.'''
        if not (await self.checkIfGameStarted(game_id)):
            return
        if not (await self.checkIfGameExists(game_id)):
            return
        if not (await self.checkIfPlayerIsCurrent(game_id, player_id)):
            return
        if not column > 0 and not column < self.GAMES[game_id].boardColumns and not column != None:
            return
        
        if len(self.GAMES[game_id].board[column]) < self.GAMES[game_id].boardRows: # Check if move is valid.
            self.GAMES[game_id].board[column].append(player_id)
            await self.explorer.ws.broadcast(
                game_id, 
                Event(ServerEvents.MAKED_TURN, {'player_id': player_id, 'column': column}), 
                [player_id]
            )  
            await self.explorer.ws.cancel_timeout_task(game_id, self.GAMES[game_id].current_player_id)
            winner = await self.checkWin(self.GAMES[game_id].board, self.GAMES[game_id].boardColumns, self.GAMES[game_id].boardRows)
            if winner:
                await self.explorer.ws.broadcast(
                    game_id, 
                    Event(ServerEvents.PLAYER_WIN, {'player_id': winner})
                )
                self.GAMES[game_id].started = False
            else:
                await self.nextPlayer(game_id)
        
    async def rematch(self, game_id: int, player_id: int) -> None:
        '''Rematches a game.'''
        if not (await self.checkIfGameExists(game_id)):
            return
        if (await self.checkIfGameStarted(game_id)):
            return
        if self.GAMES[game_id].rematch:
            await self.startGame(game_id)
            self.GAMES[game_id].rematch = False
        else:
            self.GAMES[game_id].rematch = True
            await self.explorer.ws.create_rematch_timeout_task(game_id, player_id)
            await self.explorer.ws.broadcast(game_id, Event(ServerEvents.REMATCH_REQUEST, {}), [player_id])
        
    async def closeGame(self, game_id: int) -> None:
        '''Closes a game.'''
        if not (await self.checkIfGameExists(game_id)):
            return
        del self.GAMES[game_id]
        await self.explorer.ws.close_all(game_id)
        