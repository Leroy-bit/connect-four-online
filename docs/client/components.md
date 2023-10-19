# Components

## Board
Component that represents a game board, and controls it.

**Methods:**
- `makeTurn` - emit a turn even
- `pushToBoard` - push a chip to the board
- `clear` - clear the board


## User
Component that represents a user object, and controls it.

**Properties:**
- `id` - id of the user
- `barType` - type of the turn bar, if true - turn bar is above the user name, otherwise - below
- `isCurrentUser` - if true - turn bar is active, otherwise - inactive

**Slots:**
- `name` - name of the user


## Popup
Component that represents a popup

**Slots:**
- `title` - title of the popup
- `buttons` - buttons of the popup

## PopupManager
Component that manage Popup component and simplifies the creation of popups

### Popup buttons
Popup button is an object with the following properties:
- `id` - id of the button
    - `close` - disconnect and close the MiniApp
    - `rematch` - sends a rematch request
    - `rematch_accept` - accepts a rematch request
- `text` - text of the button
- `type` - type of the button
    - `true` - button with accept color
    - `false` - button with decline color

**Methods:**
- `openPopup` - show a popup
  - `title` - title of the popup
  - `buttons` - list of [buttons](#popup-buttons) of the popup
- `closePopup` - close a popup
- `onButtonClick` - emit a `popupButtonClicked` event
  - `id` - id of the button


## Screen
Component that represents a screen

**Slots:**
- `text` - text of the screen
- `sticker` - `<img>`sticker of the screen


## ScreenManager
Component that manage Screen component and simplifies the creation of screens

**Methods:**
- `showScreen` - show a screen
  - `text` - text of the screen
  - `stickerType` - sticker type of the screen
    - `waiting` - waiting sticker
    - `error` - error sticker
- `hideScreen` - hide a screen