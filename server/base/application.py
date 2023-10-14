from aiohttp import web
from explorer import Explorer

class Application(web.Application):
    explorer: 'Explorer'


class Request(web.Request):
    '''
    Custom request class.

    Attributes:
        app: Application instance.
        user_id: User ID.
        game_id: Game ID.
        user_name: User name.
    '''

    user_id: int
    game_id: int
    user_name: str

    @property
    def app(self) -> 'Application':
        return super().app  # type: ignore
    
class View(web.View):
    '''Custom view class.

    Attributes:
        request: Request instance.
        app: Application instance.
        explorer: Explorer instance.
    '''
    @property
    def request(self) -> Request:
        return super().request  # type: ignore

    @property
    def app(self) -> 'Application':
        return self.request.app

    @property
    def explorer(self) -> 'Explorer':
        return self.app.explorer