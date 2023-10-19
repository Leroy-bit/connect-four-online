import random
from base.entity import BaseEntity
from explorer.websocket_accessor import Event
from explorer.websocket_manager import ServerEvents
from dataclasses import dataclass, asdict

@dataclass
class User:
    '''User class.
    
    Attributes:
        id: User ID.
        name: User name.
    '''
    id: int 
    name: str

class Game:
    '''Game class.

    Attributes:
        id: Game ID.
        started: Game started.
        users: Users in game.
        board: Game board.
        boardRows: Number of rows in game board.
        boardColumns: Number of columns in game board.
        current_user_id: Current user ID.
    '''

    def __init__(self, id: int, user_id: int, user_name) -> None:
        self.id: int = id
        self.started: bool = False
        self.users: dict[int, User] = {user_id: User(user_id,  user_name)}
        self.rematch: bool = False
        self.board: list[list] = []
        self.boardRows: int = 7
        self.boardColumns: int = 8
        self.current_user_id: int = None


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
    
    async def checkIfUserIsCurrent(self, game_id: int, user_id: int) -> bool:
        '''Checks if a user is the current user. Returns True if user is the current user.'''
        return self.GAMES[game_id].current_user_id == user_id
    
    async def checkIfUserInGame(self, game_id: int, user_id: int) -> bool:
        '''Checks if a user is in a game. Returns True if user is in game.'''
        return user_id in self.GAMES[game_id].users.keys()
    
    async def checkIfUsersCountIsEnough(self, game_id: int) -> bool:
        '''Checks if there are enough users in a game. Returns True if there are enough users.'''
        return len(self.GAMES[game_id].users) >= 2

    async def getAllUsers(self, game_id: int) -> list[User]:
        '''Returns all users in a game.'''
        return [asdict(user) for user in self.GAMES[game_id].users.values()]

    async def createGame(self, game_id: int, user_id: int, user_name: str) -> None:
        '''Create a new game.'''
        game = Game(game_id, user_id, user_name)
        self.GAMES[game.id] = game
        self.explorer.logger.trace(f'Game {game_id} created by {user_name}[{user_id}]')

    async def startGame(self, game_id: int) -> None:
        '''Starts a game.'''
        self.GAMES[game_id].started = True
        self.GAMES[game_id].board = []
        for _ in range(self.GAMES[game_id].boardColumns):
            self.GAMES[game_id].board.append([])
        self.GAMES[game_id].current_user_id = random.choice(list(self.GAMES[game_id].users.keys()))
        await self.explorer.ws.cancelGameTimeoutTasks(game_id)
        await self.explorer.ws.createTurnTimeoutTask(game_id, self.GAMES[game_id].current_user_id)
        await self.explorer.ws.broadcast(
            game_id, 
            Event(ServerEvents.GAME_STARTED, {'current_user_id': self.GAMES[game_id].current_user_id})
        )

    async def addUser(self, game_id: int, user_id: int, user_name: str) -> User:
        '''Adds a user to a game.'''
        user = User(user_id, user_name)
        self.GAMES[game_id].users[user_id] = user
        return user
            
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
    
    async def checkDraw(self, board: list[list[int]], columns: int, rows: int) -> bool:
        '''Checks the board for a draw.'''
        for column in range(columns):
            if len(board[column]) < rows:
                return False
        return True

    async def nextUser(self, game_id: int) -> None:
        '''Switches to the next user.'''
        users_ids = list(self.GAMES[game_id].users.keys())
        next_user_id = users_ids[users_ids.index(self.GAMES[game_id].current_user_id) - 1]
        self.GAMES[game_id].current_user_id = next_user_id
        await self.explorer.ws.createTurnTimeoutTask(game_id, next_user_id)
        await self.explorer.ws.broadcast(
            game_id, 
            Event(ServerEvents.NEXT_USER, {'current_user_id': next_user_id})
        )

    async def makeTurn(self, game_id: int, user_id: int, column: int = None) -> None:
        '''Makes a turn.'''
        if not (await self.checkIfGameStarted(game_id)):
            return
        if not (await self.checkIfGameExists(game_id)):
            return
        if not (await self.checkIfUserIsCurrent(game_id, user_id)):
            return
        if not column > 0 and not column < self.GAMES[game_id].boardColumns and not column != None:
            return
        
        if len(self.GAMES[game_id].board[column]) < self.GAMES[game_id].boardRows: # Check if move is valid.
            self.GAMES[game_id].board[column].append(user_id)
            await self.explorer.ws.broadcast(
                game_id, 
                Event(ServerEvents.MAKED_TURN, {'user_id': user_id, 'column': column}), 
                [user_id]
            )  
            await self.explorer.ws.cancelTimeoutTask(game_id, self.GAMES[game_id].current_user_id)
            winner = await self.checkWin(self.GAMES[game_id].board, self.GAMES[game_id].boardColumns, self.GAMES[game_id].boardRows)
            draw = await self.checkDraw(self.GAMES[game_id].board, self.GAMES[game_id].boardColumns, self.GAMES[game_id].boardRows)
            if winner:
                await self.explorer.ws.broadcast(
                    game_id, 
                    Event(ServerEvents.USER_WIN, {'user_id': winner})
                )
                self.GAMES[game_id].started = False
                await self.explorer.ws.createRematchTimeoutTask(game_id, winner)
            elif draw:
                await self.explorer.ws.broadcast(
                    game_id, 
                    Event(ServerEvents.DRAW, {})
                )
                self.GAMES[game_id].started = False
            else:
                await self.nextUser(game_id)
        
    async def rematch(self, game_id: int, user_id: int) -> None:
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
            await self.explorer.ws.createRematchTimeoutTask(game_id, user_id)
            await self.explorer.ws.broadcast(game_id, Event(ServerEvents.REMATCH_REQUEST, {}), [user_id])
        
    async def closeGame(self, game_id: int) -> None:
        '''Closes a game.'''
        if not (await self.checkIfGameExists(game_id)):
            return
        del self.GAMES[game_id]
        await self.explorer.ws.closeAll(game_id)
        