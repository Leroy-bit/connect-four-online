from aiohttp import web
from explorer import Explorer

class Application(web.Application):
    explorer: 'Explorer'


class Request(web.Request):
    user_id: int
    game_id: int
    user_name: str

    @property
    def app(self) -> 'Application':
        return super().app  # type: ignore
    
class View(web.View):
    @property
    def request(self) -> Request:
        return super().request  # type: ignore

    @property
    def app(self) -> 'Application':
        return self.request.app

    @property
    def explorer(self) -> 'Explorer':
        return self.app.explorer