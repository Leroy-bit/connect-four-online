# Introduction
**Welcome to the [@ConnectFourOnlineBot](https://t.me/ConnectFourOnlineBot) documentation. The bot is developed to play the game Connect Four game with a friend in a private chat.**

## Builded on

* **Server** - built on the python programming language on the **aiohttp** library using **aiohttp** asynchronous websockets. Bot uses the **aiogram** library.

* **Client** - built on the **Vue** framework.


# Setup and installation

## Setup bot in BotFather
* Create a new bot using **/newbot** command, and enable inline mode for it, write the bot token whick you received in [BOT_TOKEN](https://github.com/Leroy-bit/connect-four-online#setup-config-file) variable in config file
* Create a new mini for this bot app using **/newapp** command, write miniapp name you've created in [MINI_APP_NAME](https://github.com/Leroy-bit/connect-four-online#setup-config-file) variable in config file


## Setup config file
* BOT_TOKEN - bot token
* WEBHOOK_SECRET_TOKEN - secret token using for webhook, can be any string
* MINI_APP_NAME - mini app name that you created in **BotFather** (t.me/bot_name/**MINI_APP_NAME**)
* BASE_URL - domain on which the bot is hosted, should start with _**https://**_
* SSL_CERT - path to ssl certificate, leave empty if you want to run in http mode (or if you will use ngrok)
* SSL_PRIVATE_KEY - path to ssl private key, leave empty if you want to run in http mode (or if you will use ngrok)
* LOG_LEVEL - log level, can be **TRACE**, **DEBUG**, **INFO**, **WARNING**, **ERROR**, **CRITICAL**. [More information here](https://betterstack.com/community/guides/logging/loguru/#exploring-log-levels-in-loguru)

## Installation and building the application

**Requirements:**
* Python - 3.10 and higher
* Node js - 18.18.0 and higher
#
```bash
git clone https://github.com/Leroy-bit/connect-four-online
cd connect-four-online
pip3.10 install -r server/requirements.txt && cd client && npm install && npm run build && cd ..
```

## Run application on local machine using ngrok

**Requirements:**
* ngrok on your local machine
* registered ngrok domain (Write it in [BASE_URL](https://github.com/Leroy-bit/connect-four-online#setup-config-file) variable in config file)
#
You need to open two terminals and run the following commands in them

**First terminal**
```bash
python3.10 server/main.py
```

**Second terminal**
```bash
ngrok http --domain {your_ngrok_domain_name} 80
```

# [More documentation](https://github.com/Leroy-bit/connect-four-online/wiki/Home)







