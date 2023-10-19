![https://t.me/ConnectFourOnlineBot](https://telegra.ph/file/c7712cebf3a24eea4cc16.png)

# Introduction

**Welcome to the [@ConnectFourOnlineBot](https://t.me/ConnectFourOnlineBot). The bot is developed to play the game Connect Four game with a friend in a private chat.**

The server side of the bot is written in Python using the aiohttp library and the aiogram library for the bot itself. The client side is written in Vue.js and uses the Vite.


# Installation

**Requirements:**
- Python - 3.10 and higher
- Node js - 18.18.0 and higher

```bash
git clone https://github.com/Leroy-bit/connect-four-online
cd connect-four-online
pip3.10 install -r server/requirements.txt && cd client && npm install && npm run build && cd ..
```


# Configuration

## Setup bot in BotFather
- Create a new bot using **/newbot** command, and enable inline mode for it, write the bot token which you received in [BOT_TOKEN](#setup-config-file) variable in config file
- Create a new Mini App for this bot app using **/newapp** command, write miniapp name you've created in [MINI_APP_NAME](#setup-config-file) variable in config file

## Setup config file
- `BASE_URL` - domain on which the bot is hosted, should start with _**https://**_
- `BOT_TOKEN` - bot token
- `WEBHOOK_SECRET_TOKEN` - secret token using for webhook, can be any string
- `MINI_APP_NAME` - mini app name that you created in **BotFather** (t.me/bot_name/**MINI_APP_NAME**)
- `SSL_CERT` - path to ssl certificate, leave empty if you want to run in http mode (or if you will use ngrok)
- `SSL_PRIVATE_KEY` - path to ssl private key, leave empty if you want to run in http mode (or if you will use ngrok)
- `LOG_LEVEL` - log level, can be **TRACE**, **DEBUG**, **INFO**, **WARNING**, **ERROR**, **CRITICAL**. [More information here](https://betterstack.com/community/guides/logging/loguru/#exploring-log-levels-in-loguru)


# Running the application

## Running with ngrok

**Requirements:**
- [ngrok](https://ngrok.com/download) installed on your local machine
- registered [ngrok domain](https://ngrok.com/docs/guides/how-to-set-up-a-custom-domain/) (Write it in [BASE_URL](#setup-config-file) variable in config file)

You need to open two terminals and run the following commands in them

**First terminal**
```bash
python3.10 server/main.py
```

**Second terminal**
```bash
ngrok http --domain {your_ngrok_domain_name} 80
```

# [Extended documentation](https://leroy-bit.github.io/connect-four-online)







