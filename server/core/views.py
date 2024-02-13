from base.application import View
import traceback
    

class WebSocketView(View):
    '''
    View for WebSocket connection.
    '''
    async def get(self):
        try:
            await self.explorer.ws.open(self.request)
            await self.explorer.ws_manager.handleConnection(self.request.game_id, self.request.user_id)
            await self.explorer.ws_manager.handleDisconnect(self.request.game_id, self.request.user_id)
            # return self.explorer.ws.connections[self.request.game_id][self.request.user_id].ws
        except Exception as exc:
            self.explorer.logger.error(exc)
            self.explorer.logger.error(traceback.format_exc())