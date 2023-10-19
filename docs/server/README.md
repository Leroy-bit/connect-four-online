## Server is builted on python 3.10 <!-- {docsify-ignore} -->

## Structure of the server <!-- {docsify-ignore} -->
- [Explorer](server/explorer.md) - **Class that can be accessed from <mark>anywhere</mark> in the application and contains all its available entities**
- [Base](server/base.md) - **Сontains wrappers or base classes of entities formatted for convenient work with the application**
- [Core](server/core.md) - **Contains views and middlewares for aiohttp server**

#### Builted on: <!-- {docsify-ignore} -->
- [aiohttp[3.8.6]](https://docs.aiohttp.org/en/stable/)
- [aiogram[3.1.1]](https://docs.aiogram.dev/en/v3.1.1/)
- [loguru[0.7.0]](https://loguru.readthedocs.io/en/stable/)    

#### Running the server
!> **You must be in the `server` directory**

**Requirements:**
- Python - 3.10 and higher

**Install requirement libraries**
```bash
pip3.10 install -r requirements.txt
```

***

##### Run server
!> **You must [build](client/#build-for-production) the client before running the client**

```bash
python3.10 main.py
```

