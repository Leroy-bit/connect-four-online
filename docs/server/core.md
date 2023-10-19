# Core <!-- {docsify-ignore} -->
**Contains views and middlewares for aiohttp server**


## Views
Contains views for aiohttp server

### MiniAppView
> class MiniAppView([View](server/base#view))

Processes the MiniApp request and returns the builded front-end


### WebSocketView
> class WebSocketView([View](server/base#view))

Processes the WebSocket connection and pass data to the WebSocketManager



## Setup
Contains views and middlewares setup for aiohttp server

### setup_routes
> def setup_routes(app: [Application](server/base#application))

Binds Routes to their Views

**Parameters:**
- `app`_: [Application](server/base#application)_ - aiohttp application


### setup_middlewares
> def setup_middlewares(app: [Application](server/base#application))

Setup middlewares

**Parameters:**
- `app`_: [Application](server/base#application)_ - aiohttp application



## Middlewares
Contains a middlewares for aiohttp server

### WebSocketMiddleware
> async def WebAppMiddleware(request: Request, handler: typing.Callable[[Request], typing.Awaitable[web.Response]]) -> web.Response:

Middleware that prepare request data and check web app init data for validity, created with aiohttp.web.middleware decorator



