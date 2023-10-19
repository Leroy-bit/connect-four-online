# Base <!-- {docsify-ignore} -->
**Сontains wrappers or base classes of entities formatted for convenient work with the application**

## BaseEntity
> class BaseEntity

Base class for all entities, which adds the explorer to the entity

**Attributes:**
- `explorer`_: [Explorer](server/explorer.md)_


## Application
> class Application

Wrapper for the aiohttp application, which adds the explorer to the application

**Attributes:**
- `explorer`_: [Explorer](server/explorer.md)_


## Request
> class Request

Wrapper for the aiohttp request, which adds the explorer to the request and 
adds the variables for user data

**Attributes:**
- `explorer`_: [Explorer](server/explorer.md)_
- `user_id`_: int_ - user id
- `user_name`_: str_ - user name
- `game_id`_: int_ - game id


## View
> class View

Wrapper for aiohttp.web.View, base class for all views, which adds the explorer, app variables to the view, and simplifies
access to the request

**Attributes:**
- `explorer`_: [Explorer](server/explorer.md)_
- `app`_: [Application](#application)_
- `request`_: [Request](#request)_
