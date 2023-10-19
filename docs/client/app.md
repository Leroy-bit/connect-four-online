# Component
main component that conrols all app

## Variables

- `me` - this(self) user Object
- `opponent` - opponent user Object
- `currentUserId` - id of current user
- `serverEvents` - server events Object
- `clientEvents` - client events Object
- `gameStarted` - is game started
- `connected` - is user connected to server
- `hasMoved` - has user moved
- `waitingTimeout` - waiting timeout in seconds
- `waitingTimeoutId` - id of waiting timeout, returned by `setTimeout` function

## Constants
- `socketUrl` - url of WebSocket server
- `socket` - `WebSocket` object

## Methods
- `sendEvent` - send event to server with `WebSocket`
  - `event` - event name string
  - `data` - event data Object


- `makeTurn` - listener function that make turn in game
  - `column` - column number


- `nextUser` - change current user
  - `userId` - id of next user


- `onPopupClicked` - listener function that handle popup click
  - `id` - id of clicked popup


- `disconnect` - disconnect from server and close the MiniApp

## Mounted
In this function `WebSocket` event listeners and [constants](#constants) configured

## Localization
For localization [`vue-i18n`](https://kazupon.github.io/vue-i18n/) library is used. To add new language you need to create new file in `client/src/locales` directory with name `{language}.json` and add it to `client/src/locales/index.js` file. Then you need to add new language to `client/src/components/Popup.vue` file in `locales` array. After that you can use `$t` function in your component.