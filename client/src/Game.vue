<template>
      <ScreenManager ref="screenManager"></ScreenManager>
      <PopupManager @popupButtonClicked="onPopupButtonClicked" ref="popupManager" />
      <User v-show="gameStarted" :id="opponent.id" :name="opponent.name" :barType="false" :isCurrentUser="opponent.id == currentUserId">
          {{opponent.name}}
      </User> 
      <Board v-show="gameStarted" @makeTurn="makeTurn" ref="board"/>
      <User v-show="gameStarted" :id="me.id" :name="me.name" :barType="true" :isCurrentUser="me.id == currentUserId">
        {{ this.$t('you') }}
      </User>
</template>

<script>
import Board from './components/Board.vue'
import User from './components/User.vue'
import ScreenManager from './components/ScreenManager.vue'
import PopupManager from './components/PopupManager.vue'

const socketUrl = 'wss://' + window.location.host + '/ws?' + window.Telegram.WebApp.initData
const socket = window.Telegram.WebApp.initDataUnsafe.chat_type == "private" ? new WebSocket(socketUrl) : undefined

export default {
  data () {
    return {
            me: window.Telegram.WebApp.initDataUnsafe.chat_type == "private" ? {id: window.Telegram.WebApp.initDataUnsafe.user.id, name: window.Telegram.WebApp.initDataUnsafe.user.first_name} : undefined,
            opponent: {},
            currentUserId: 1,
            serverEvents: {
                CONNECTED: 'CONNECTED',
                DISCONNECTED: 'DISCONNECTED',
                MAKED_TURN: 'MAKED_TURN',
                USER_JOINED: 'USER_JOINED',
                USER_DISCONNECTED: 'USER_DISCONNECTED',
                GAME_STARTED: 'GAME_STARTED',
                NEXT_USER: 'NEXT_USER',
                REMATCH_REQUEST: 'REMATCH_REQUEST',
                USER_WIN: 'USER_WIN',
                DRAW: 'DRAW'
            },
            clientEvents: {
                MAKE_TURN: 'MAKE_TURN',
                DISCONNECT: 'DISCONNECT',
                REMATCH: 'REMATCH'
            },
            gameStarted: false,
            connected: false,
            hasMoved: false,
            waitingTimeout: 44,
            waitingTimeoutId: undefined

        }
  },

  components: {
    'Board': Board,
    'User': User,
    'PopupManager': PopupManager,
    'ScreenManager': ScreenManager
  },

  methods: {
    sendEvent(event, data) {
      if (this.connected) {
        socket.send(JSON.stringify({'event': event, 'data': data}))
        console.log('[SEND EVENT]('+ event +')' + JSON.stringify(data))
      }
    },
    makeTurn(column) {
      if (this.me.id == this.currentUserId && !this.hasMoved){
        this.hasMoved = true
        this.$refs.board.pushToBoard(0, column)
        this.sendEvent(this.clientEvents.MAKE_TURN, {column: column})
      }
    },
    nextUser(userId) {
      this.currentUserId = userId
      this.hasMoved = false
    },
    onPopupButtonClicked(id) {
      if (id == 'close') {
        this.$refs.popupManager.closePopup()
        window.Telegram.WebApp.close()
        } 
      else if (id == 'rematch') {
        this.$refs.popupManager.openPopup(this.$t('popups.text.waitingOpponentConfirmation') + '...', [])
        this.sendEvent(this.clientEvents.REMATCH, {})
        } 
      else if (id == 'rematch_accept') {
        this.sendEvent(this.clientEvents.REMATCH, {})
        this.$refs.popupManager.closePopup()
        }
    },
    disconnect() {
      window.Telegram.WebApp.close()
    }
  },

  provide: {
    columns: 8,
    rows: 7,
  },

  mounted() {
    if (window.Telegram.WebApp.initDataUnsafe.chat_type == "private") {
      
      this.$refs.screenManager.showScreen(this.$t("screens.waiting"), 'waiting')
      window.Telegram.WebApp.onClose = () => {
        this.sendEvent(this.clientEvents.DISCONNECT, {})
      }

      socket.onmessage = (message) => {
      let data = JSON.parse(message.data)
      console.log('[RECIEVE EVENT]('+ data.event +')' + JSON.stringify(data.data))

      if (data.event == this.serverEvents.CONNECTED) {
        
        this.connected = true
        if (data.data.users) {
          this.opponent = data.data.users[0]
        }
        else {
          this.waitingTimeoutId = setTimeout(() => {
            window.Telegram.WebApp.close()
          }, this.waitingTimeout * 1000)

        }
      }
      else if (data.event == this.serverEvents.USER_JOINED) {
        this.opponent = data.data
        clearTimeout(this.waitingTimeoutId)
      }
      else if (data.event == this.serverEvents.GAME_STARTED) {
        window.Telegram.WebApp.enableClosingConfirmation()
        this.$refs.screenManager.hideScreen()
        this.$refs.popupManager.closePopup()
        this.$refs.board.clearBoard()
        this.gameStarted = true
        this.nextUser(data.data.current_user_id)
      }
      else if (data.event == this.serverEvents.MAKED_TURN) {
        this.$refs.board.pushToBoard(data.data.user_id, data.data.column)
      }
      else if (data.event == this.serverEvents.USER_WIN) {
        let text = data.data.user_id == this.me.id ? this.$t("win") : this.$t("lose")
        setTimeout(() => {
          this.$refs.popupManager.openPopup(text, [{id: 'rematch', text: this.$t('popups.buttons.rematch'), type: true}, {id: 'close', text: this.$t('popups.buttons.disconnect'), type: false}])
        }, 500)
      }
      else if (data.event == this.serverEvents.DRAW) {
        setTimeout(() => {
          this.$refs.popupManager.openPopup(this.$t("draw"), [{id: 'rematch', text: this.$t('popups.buttons.rematch'), type: true}, {id: 'close', text: this.$t('popups.buttons.disconnect'), type: false}])
        }, 500)
      }
      else if (data.event == this.serverEvents.NEXT_USER) { 
        this.nextUser(data.data.current_user_id)
      }
      else if (data.event == this.serverEvents.USER_DISCONNECTED) {
        if (data.data.reason) {
          this.$refs.popupManager.openPopup(this.$t('popups.text.opponentDisconnectedReason', [data.data.reason]), [{id: 'close', text: this.$t('popups.buttons.close'), type: true}])

        }
        else {
          this.$refs.popupManager.openPopup(this.$t('popups.text.opponentDisconnected'), [{id: 'close', text: this.$t('popups.buttons.close'), type: true}])
        }
      }
      else if (data.event == this.serverEvents.REMATCH_REQUEST) {
        this.$refs.popupManager.openPopup(this.$t('popups.text.opponentRematch'), [{id: 'rematch', text: this.$t('popups.buttons.accept'), type: true}, {id: 'close', text: this.$t('popups.buttons.decline'), type: false}])
      }
      else if (data.event == this.serverEvents.DISCONNECTED) {
        let reason = data.data.reason
        this.$refs.popupManager.openPopup(this.$t('popups.text.youDisconnected') + ': ' + reason, [{id: 'close', text: this.$t('popups.buttons.close'), type: true}])
      }
    }
  }
  else {
    this.$refs.screenManager.showScreen(this.$t("screens.chatError"), 'error')
  } 
      
  }

}
</script>