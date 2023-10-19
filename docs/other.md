# <!-- {docsify-ignore} -->
# Web Socket Events

## Player object
> Example: `{ id: 1, name: 'Player 1' }`

- `id` - id of the player
- `name` - name of the player

## Server Events
- `CONNECTED` - Sending to user when he connected to the server
    - `players` - list of [players](#player-object) in the game, sends only if user is not first


- `PLAYER_JOINED` - Sending to all players when new player joined to the game
    - `id` - id of the player
    - `name` - name of the player


- `PLAYER_DISCONNECTED` - Sending to all players when other player disconnected from the game
    - `id` - id of the player
    - `reason` - Optional. Sends only if user disconnected by server. Has one of the [Disconnect Reasons](#disconnect-reasons)


- `GAME_STARTED` - Sending to all players when game started
    - `current_player_id` - id of the current player, randomly selected


- `NEXT_PLAYER` - Sending to all players when the current player changed
    - `current_player_id` - id of the current player


- `MAKED_TURN` - Sending to all players when the player made a turn
    - `player_id` - id of the player
    - `column` - column number


- `PLAYER_WIN` - Sending to all players when the player won
    - `player_id` - id of the player


- `DRAW` - Sending to all players when the game ended in a draw


- `REMATCH_REQUEST` - Sending to all players when the player wants to start a rematch


- `DISCONNECTED` - Sending to the player who was disconnected
    - `reason` - Optional. Sends only if user disconnected by server. Has one of the [Disconnect Reasons](#disconnect-reasons)

## Client Events
- `MAKE_TURN` - Sending to the server when the player made a turn
    - `column` - column number


- `REMATCH` - Sending to the server when the player wants to start a rematch, or accept a rematch request


- `DISCONNECT` - Sending to the server when the player is disconnecting from the game


## Disconnect Reasons
- `TURN_TIMEOUT` - timeout for the player to make a turn
- `WAITING_FOR_PLAYER_TIMEOUT` - timeout for the player to wait fot the second player connection
- `REMATCH_TIMEOUT` - timeout for the player to accept the rematch
