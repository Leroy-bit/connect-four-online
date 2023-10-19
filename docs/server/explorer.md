# Explorer <!-- {docsify-ignore} -->
> class Explorer
> 
**class that can be accessed from anywhere in the application and contains all its available entities**
### Entities
- Accessor - controls all processes related to the entity
- Manager - combines and controls accessors

**Attributes:**
- `app`_: [Application](server/base.md#application)_ - aiohttp application
- `game_accessor`_: [GameAccessor](server/explorer.md#gameaccessor)_
- `ws`_: [WebSocketAccessor](server/explorer.md#websocketaccessor)_
- `ws_manager`_: [WebSocketManager](server/explorer.md#websocketmanager)_
- `bot_accessor`_: [BotAccessor](server/explorer.md#botaccessor)_
- `logger`*: loguru._logger.Logger*


## GameAccessor
> class GameAccessor([BaseEntity](server/base.md#baseentity))

Controls all processes related to the game mechanics and its users


### Game
> class Game

Game class that contains all game information
**Attributes:**
- `id` - game id
- `started` - game status
- `users` - list of [users](#user) in the game
- `board` - [board](#board) of the game
- `boardRows` - number of rows in the board
- `boardColumns` - number of columns in the board
- `current_user_id` - id of the current user


### User
> class User

User class that contains all user information
**Attributes:**
- `id` - user id
- `name` - user name


### GAMES
> GAMES: dict[int, Game]

Dictionary that contains all [games](#game) in the application


### createGame
> async def createGame(game_id: int, user_id: int, user_name: str)

Creates a new game and adds it to the GAMES dictionary

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id
- `user_name`_: str_ - user name


### startGame
> async def startGame(game_id: int)

Starts the game

**Parameters:**
- `game_id`_: int_ - game id


### addUser
> async def addUser(game_id: int, user_id: int, user_name: str)

Adds a user to the game

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id
- `user_name`_: str_ - user name


### checkWin
> async def checkWin(board: list[list[int]], columns: int, rows: int) -> int:

Check if there is a winner on the board

**Parameters:**
- `board`_: list[list[int]]_ - board of the game
- `columns`_: int_ - number of columns in the board
- `rows`_: int_ - number of rows in the board

**Returns:**
- `int` - id of the winner, False if there is no winner


### checkDraw
> async def checkDraw(board: list[list[int]], columns: int, rows: int) -> bool:

Check if there is a draw on the board

**Parameters:**
- `board`_: list[list[int]]_ - board of the game
- `columns`_: int_ - number of columns in the board
- `rows`_: int_ - number of rows in the board

**Returns:**
- `bool` - True if there is a draw, False otherwise


### nextUser
> async def nextUser(game_id: int)

Changes the current user to the next one

**Parameters:**
- `game_id`_: int_ - game id


### makeTurn
> async def makeTurn(game_id: int, user_id: int, column: int)

Makes a turn for the current user, checks if column is valid and if the game is over

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id
- `column`_: int_ - column number


### rematch
> async def rematch(game_id: int)

Starts a rematch for the game

**Parameters:**
- `game_id`_: int_ - game id


### closeGame
> async def closeGame(game_id: int)

Deletes the game and closes the connection for all users

**Parameters:**
- `game_id`_: int_ - game id


### checkIfGameExists
> async def checkIfGameExists(game_id: int) -> bool:

Checks if the game exists

**Parameters:**
- `game_id`_: int_ - game id

**Returns:**
- `bool` - True if the game exists, False otherwise


### checkIfUserInGame
> async def checkIfUserInGame(game_id: int, user_id: int) -> bool:

Checks if the user is in the game

**Parameters:**
- `game_id`_: int_ - game id

**Returns:**
- `bool` - True if the user is in the game, False otherwise


### checkIfUserIsCurrent
> async def checkIfUserIsCurrent(game_id: int, user_id: int) -> bool:

Checks if the user is the current user

**Parameters:**
- `game_id`_: int_ - game id

**Returns:**
- `bool` - True if the user is the current user, False otherwise


### checkIfGameStarted
> async def checkIfGameStarted(game_id: int) -> bool:

Checks if the game started

**Parameters:**
- `game_id`_: int_ - game id

**Returns:**
- `bool` - True if the game started, False otherwise


### checkIfUsersCountIsEnough
> async def checkIfUsersCountIsEnough(game_id: int) -> bool:

Checks if the number of users in the game no more than 2

**Parameters:**
- `game_id`_: int_ - game id

**Returns:**
- `bool` - True if the number of users in the game >= 2, False otherwise


## WebSocketAccessor
> class WebSocketAccessor([BaseEntity](server/base.md#baseentity))

Сontrols the connection of users to the game via WebSocket


### TURN_TIMEOUT
> TURN_TIMEOUT: int

Time in seconds for the user to make a turn


### WAITING_FOR_USER_TIMEOUT
> WAITING_FOR_USER_TIMEOUT: int

Time in seconds for the user to join the game


### REMATCH_TIMEOUT
> REMATCH_TIMEOUT: int

Time in seconds for the user to accept the rematch


### Event
> class Event

Event class that contains all event information

**Attributes:**
- `event`_: str_ - event name, see below
- `data`_: str_ - event data, see below

Detail about websocket events [here](general.md#websocket-events)


### Connection
> class Connection

Connection class that contains all connection information

**Attributes:**
- `ws`_: aiohttp.WebSocketResponce_ - websocket connection
- `timeout_task`_: asyncio.Task_ - task that controls the timeout of connection
- `close_callback`_: Callable_ - callback that will be called when the connection is closed


### connections
> connections: dict[int, Connection]

Dictionary that contains all connections


### open
> async def open(request: [base.application.Request](#request))

Handles the WebSocket connection from request and adds it to the connections,
checks if the game exists and if the user is in the game

**Parameters:**
- `request`_: [base.application.Request](#request)_ - request from the client


### close
> async def close(game_id: int, user_id: int, reason: str | None)

Wrapper for the [_close](#_close) method, if reason is passed - broadcasts the reason to all users,
also check if the game exists and if the user is in the game

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id
- `reason`(Optional)_: str | None_  - reason for closing the connection


### closeAll
> async def closeAll(game_id: int)

Wrapper for the [_close](#_close) method, closes the connection for all users,
if reason is passed - broadcasts the reason to all users, also check if the game exists

**Parameters:**
- `game_id`_: int_ - game id
- `reason`(Optional)_: str | None_  - reason for closing the connection


### _close
> async def _close(game_id: int, user_id: int)

Closes the connection for the user, without checking if the game exists and if the user is in the game,
also cancel the connection timeout task

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### send
> async def send(game_id: int, event: [Event](#event))

Sends an event to the single user

**Parameters:**
- `game_id`_: int_ - game id
- `event`_: [Event](#event)_ - event to send


### broadcast
> async def broadcast(game_id: int, event: [Event](#event), except_of: list[int])

Sends an event to all users in the game

**Parameters:**
- `game_id`_: int_ - game id
- `event`_: [Event](#event)_ - event to send
- `except_of`_: list[int]_ - list of user ids to exclude from sending


### readStream
> async def readStream(game_id: int, user_id: int) -> typing.AsyncIterable[Event]

Reads the stream of raw events from the user

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id

**Yields:**
- `Event` - event from the user


### isClosed
> async def isClosed(self, game_id: int, user_id: int) -> bool:

Checks if the connection is closed

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id

**Returns:**
- `bool` - True if the connection is closed, False otherwise


### createTurnTimeoutTask
> async def createTurnTimeoutTask(game_id: int, user_id: int)

Creates a task that will close the connection if the user does not make a turn in time

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### createWaitingForUserTimeoutTask
> async def createWaitingForUserTimeoutTask(game_id: int, user_id: int)

Creates a task that will close the connection if the second user does not join the game in time

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### createRematchTimeoutTask
> async def createRematchTimeoutTask(game_id: int, user_id: int)

Creates a task that will close the connection if the user does not accept the rematch in time

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### createTimeoutTask
> async def createTimeoutTask(timeout: int, callback: typing.Callable, **kwargs):

Creates a task that will call the callback after the timeout, wrapper for the [_createTimeoutTask](#_createTimeoutTask) method

**Parameters:**
- `timeout`_: int_ - timeout in seconds
- `callback`_: typing.Callable_ - callback to call after the timeout
- `kwargs`_: dict_ - arguments for the callback
    - `game_id`_: int_ - game id
    - `user_id`_: int_ - user id
    - `reason`(Optional)_: str | None_  - reason for closing the connection


### cancelTimeoutTask
> async def cancelTimeoutTask(game_id: int, user_id: int):

Cancels the connection timeout task

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### cancelGameTimeoutTasks
> async def cancelGameTimeoutTasks(game_id: int):

Cancels timeout tasks for all connections in the game

**Parameters:**
- `game_id`_: int_ - game id


### _createTimeoutTask
> async def _createTimeoutTask(callback: typing.Callable, timeout: int, **kwargs):

Creates a task that will call the callback after the timeout

**Parameters:**
- `callback`_: typing.Callable_ - callback to call after the timeout
- `timeout`_: int_ - timeout in seconds
- `kwargs`_: dict_ - arguments for the callback



## WebSocketManager
> class WebSocketManager([BaseEntity](server/base.md#baseentity))

Class that controls the WebSocket connections and game processes


### handleConnection
> async def handleConnection(game_id: int, user_id: int)

Handles the prepared client events

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id


### handleDisconnect
> async def handleDisconnect(game_id: int, user_id: int)

Handles the client disconnect

**Parameters:**
- `game_id`_: int_ - game id
- `user_id`_: int_ - user id



## BotAccessor
> class BotAccessor([BaseEntity](server/base.md#baseentity))

Controls the telegram bot. Works on webhook registered on the aiohttp server


### setup
> def setup()

Sets up the bot, and all its handlers, commands, etc.


### registerHandlers
> def registerHandlers()

Registers handlers for the bot


### setupBotCommands
> async def setupBotCommands() -> list[types.BotCommand]:

Sets up the bot commands

**Returns:**
- `list[types.BotCommand]` - list of bot commands


### checkUserData
> async def checkUserData(initData: str) -> aiogram.utils.web_app.WebAppInitData:

Wrapper for the aiogram.utils.web_app.safe_parse_webapp_init_data method

**Parameters:**
- `initData`_: str_ - init data from the client

**Returns:**
- `aiogram.utils.web_app.WebAppInitData` - parsed init data
