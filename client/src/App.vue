<template>
      <ScreenManager ref="screenManager"></ScreenManager>
      <PopupManager @popupButtonClicked="onPopupButtonClicked" ref="popupManager" />
      <Player v-show="game_started" :id="opponent.id" :name="opponent.name" :bar_type="false" :isCurrentPlayer="opponent.id == currentPlayerId">
          {{opponent.name}}
      </Player> 
      <Board v-show="game_started" @makeTurn="makeTurn" ref="board"/>
      <Player v-show="game_started" :id="me.id" :name="me.name" :bar_type="true" :isCurrentPlayer="me.id == currentPlayerId">
        {{ this.$t('you') }}
      </Player>
</template>

<script>
import Board from './components/Board.vue'
import Player from './components/Player.vue'
import ScreenManager from './components/ScreenManager.vue'
import PopupManager from './components/PopupManager.vue'

const socket_url = 'wss://' + window.location.host + ':443/ws?' + window.Telegram.WebApp.initData
const socket = window.Telegram.WebApp.initDataUnsafe.chat_type == "private" ? new WebSocket(socket_url) : undefined

export default {
  data () {
    return {
            me: {id: window.Telegram.WebApp.initDataUnsafe.user.id, name: window.Telegram.WebApp.initDataUnsafe.user.first_name},
            opponent: {},
            currentPlayerId: 1,
            serverEvents: {
                CONNECTED: 'CONNECTED',
                DISCONNECTED: 'DISCONNECTED',
                MAKED_TURN: 'MAKED_TURN',
                PLAYER_JOINED: 'PLAYER_JOINED',
                PLAYER_DISCONNECTED: 'PLAYER_DISCONNECTED',
                GAME_STARTED: 'GAME_STARTED',
                NEXT_PLAYER: 'NEXT_PLAYER',
                REMATCH_REQUEST: 'REMATCH_REQUEST',
                PLAYER_WIN: 'PLAYER_WIN'
            },
            clientEvents: {
                MAKE_TURN: 'MAKE_TURN',
                DISCONNECT: 'DISCONNECT',
                REMATCH: 'REMATCH'
            },
            game_started: false,
            connected: false,
            hasMoved: false

        }
  },

  components: {
    'Board': Board,
    'Player': Player,
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
      if (this.me.id == this.currentPlayerId && !this.hasMoved){
        this.hasMoved = true
        this.$refs.board.pushToBoard(0, column)
        this.sendEvent(this.clientEvents.MAKE_TURN, {column: column})
      }
    },
    nextPlayer(playerId) {
      this.currentPlayerId = playerId
      this.hasMoved = false
    },
    disconnect() {
      window.Telegram.WebApp.close()
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
      else if (id == 'disconnect') {
        this.$refs.popupManager.closePopup()
        this.disconnect()
        }
    }
  },

  provide: {
    columns: 8,
    rows: 7,
  },

  mounted() {
    if (window.Telegram.WebApp.initDataUnsafe.chat_type == "private") {
      
      window.Telegram.WebApp.onClose = () => {
        this.sendEvent(this.clientEvents.DISCONNECT, {})
      }
      
      this.$refs.screenManager.showScreen(this.$t("screens.waiting"), 'waiting')

      socket.onmessage = (message) => {
      let data = JSON.parse(message.data)
      console.log('[RECIEVE EVENT]('+ data.event +')' + JSON.stringify(data.data))
      if (data.event == this.serverEvents.CONNECTED) {
        this.connected = true
        if (data.data.players) {
          this.opponent = data.data.players[0]
        }
      }
    else if (data.event == this.serverEvents.PLAYER_JOINED) {
      window.Telegram.WebApp.enableClosingConfirmation()
      this.opponent = data.data
      }
    else if (data.event == this.serverEvents.GAME_STARTED) {
      this.$refs.screenManager.hideScreen()
      this.$refs.popupManager.closePopup()
      this.$refs.board.clearBoard()
      this.game_started = true
      this.nextPlayer(data.data.current_player_id)
      }
    else if (data.event == this.serverEvents.MAKED_TURN) {
      this.$refs.board.pushToBoard(data.data.player_id, data.data.column)
      }
    else if (data.event == this.serverEvents.PLAYER_WIN) {
      let text = data.data.player_id == this.me.id ? this.$t("win") : this.$t("lose")
      setTimeout(() => {
        this.$refs.popupManager.openPopup(text, [{id: 'rematch', text: this.$t('popups.buttons.rematch'), type: true}, {id: 'disconnect', text: this.$t('popups.buttons.disconnect'), type: false}])
      }, 500)
      }
    else if (data.event == this.serverEvents.NEXT_PLAYER) { 
      this.nextPlayer(data.data.current_player_id)
      }
    else if (data.event == this.serverEvents.PLAYER_DISCONNECTED) {
      this.$refs.popupManager.openPopup(this.$t('popups.text.opponentDisconnected'), [{id: 'close', text: this.$t('popups.buttons.close'), type: true}])
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