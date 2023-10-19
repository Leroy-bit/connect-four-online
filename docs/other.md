# <!-- {docsify-ignore} -->
# Web Socket Events

## User object
> Example: `{ id: 1, name: 'User 1' }`

- `id` - id of the user
- `name` - name of the user

## Server Events
- `CONNECTED` - Sending to user when he connected to the server
    - `users` - list of [users](#user-object) in the game, sends only if user is not first


- `USER_JOINED` - Sending to all users when new user joined to the game
    - `id` - id of the user
    - `name` - name of the user


- `USER_DISCONNECTED` - Sending to all users when other user disconnected from the game
    - `id` - id of the user
    - `reason` - Optional. Sends only if user disconnected by server. Has one of the [Disconnect Reasons](#disconnect-reasons)


- `GAME_STARTED` - Sending to all users when game started
    - `current_user_id` - id of the current user, randomly selected


- `NEXT_USER` - Sending to all users when the current user changed
    - `current_user_id` - id of the current user


- `MAKED_TURN` - Sending to all users when the user made a turn
    - `user_id` - id of the user
    - `column` - column number


- `USER_WIN` - Sending to all users when the user won
    - `user_id` - id of the user


- `DRAW` - Sending to all users when the game ended in a draw


- `REMATCH_REQUEST` - Sending to all users when the user wants to start a rematch


- `DISCONNECTED` - Sending to the user who was disconnected
    - `reason` - Optional. Sends only if user disconnected by server. Has one of the [Disconnect Reasons](#disconnect-reasons)

## Client Events
- `MAKE_TURN` - Sending to the server when the user made a turn
    - `column` - column number


- `REMATCH` - Sending to the server when the user wants to start a rematch, or accept a rematch request


- `DISCONNECT` - Sending to the server when the user is disconnecting from the game


## Disconnect Reasons
- `TURN_TIMEOUT` - timeout for the user to make a turn
- `WAITING_FOR_USER_TIMEOUT` - timeout for the user to wait fot the second user connection
- `REMATCH_TIMEOUT` - timeout for the user to accept the rematch
