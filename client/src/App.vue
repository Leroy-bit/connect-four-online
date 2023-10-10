<template>
      <PopupManager @popupButtonClicked="onPopupButtonClicked" ref="popupManager" />
      <WaitingScreen v-show="!game_started && !opponent.id"/>
      <Player v-show="game_started" :id="opponent.id" :name="opponent.name" :bar_type="false" :isCurrentPlayer="opponent.id == currentPlayerId">
          {{opponent.name}}
      </Player> 
      <Board v-show="game_started" @makeTurn="makeTurn" ref="board"/>
      <Player v-show="game_started" :id="me.id" :name="me.name" :bar_type="true" :isCurrentPlayer="me.id == currentPlayerId">
        YOU
      </Player>
</template>

<script>
import Board from './components/Board.vue'
import Player from './components/Player.vue'
import WaitingScreen from './components/WaitingScreen.vue'
import PopupManager from './components/PopupManager.vue'
const socket_url = 'wss://' + window.location.host + '/ws?' + window.Telegram.WebApp.initData
const socket =  'MozWebSocket' in window ? new MozWebSocket(socket_url) : new WebSocket(socket_url)

export default {
  data () {
    return {
            me: {id: window.Telegram.WebApp.initDataUnsafe.user.id, name: window.Telegram.WebApp.initDataUnsafe.user.first_name},
            opponent: {},
            currentPlayerId: 1,
            serverEvents: {
                CONNECT: 'CONNECT',
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
    'WaitingScreen': WaitingScreen,
    'PopupManager': PopupManager
  },

  methods: {
    sendEvent(event, data) {
      if (this.connected) {
        socket.send(JSON.stringify({'event': event, 'data': data}))
        console.log('[sendEvent]('+ event +')' + JSON.stringify(data))
      }
      else {
        console.log('[sendEvent]('+ event +')' + JSON.stringify(data) + ' - not connected')
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
        this.$refs.popupManager.openPopup('Waiting for opponent confirmation...', [])
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
    window.Telegram.WebApp.enableClosingConfirmation()
    window.Telegram.WebApp.onClose = () => {
      this.sendEvent(this.clientEvents.DISCONNECT, {})
    }

    socket.onmessage = (message) => {
      let data = JSON.parse(message.data)
      console.log('[RECIEVE]('+ data.event +')' + JSON.stringify(data.data))
      if (data.event == this.serverEvents.CONNECT) {
        this.connected = true
        if (data.data.players) {
          this.opponent = data.data.players[0]
        }
      }
    else if (data.event == this.serverEvents.PLAYER_JOINED) {
      this.opponent = data.data
      }
    else if (data.event == this.serverEvents.GAME_STARTED) {
      this.$refs.popupManager.closePopup()
      this.$refs.board.clearBoard()
      this.game_started = true
      this.nextPlayer(data.data['current_player_id'])
      }
    else if (data.event == this.serverEvents.MAKED_TURN) {
      this.$refs.board.pushToBoard(data.data.player_id, data.data.column)
      }
    else if (data.event == this.serverEvents.PLAYER_WIN) {
      this.$refs.popupManager.openPopup('You lose', [{id: 'rematch', text: 'Rematch', type: true}, {id: 'disconnect', text: 'DISCONNECT', type: false}])
      }
    else if (data.event == this.serverEvents.NEXT_PLAYER) { 
      this.nextPlayer(data.data['current_player_id'])
      }
    else if (data.event == this.serverEvents.PLAYER_DISCONNECTED) {
      this.$refs.popupManager.openPopup('Opponent disconnected', [{id: 'close', text: 'Close', type: true}])
      }
    else if (data.event == this.serverEvents.REMATCH_REQUEST) {
      this.$refs.popupManager.openPopup('Opponent wants to rematch', [{id: 'rematch', text: 'Accept', type: true}, {id: 'close', text: 'Decline', type: false}])
      }
    }
  }

}
</script>