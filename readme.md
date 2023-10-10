# Introduction
**Welcome to the [@ConnectFourOnlineBot](https://t.me/ConnectFourOnlineBot) documentation. The bot is developed to play the game Connect Four with a friend in a private chat.**

## Build

* **Server** - built on the python programming language on the **aiohttp** library using **aiohttp** asynchronous websockets. Bot uses the **aiogram** library.

* **Client** - built on the **Vue** framework.


# Setup and installation
## Setup config file
* BOT_TOKEN - bot token
* WEBHOOK_SECRET_TOKEN - secret token using for webhook
* MINI_APP_NAME - mini app name that you have done in **BotFather**
* BASE_URL - your ngrok url

## Installation and building the application
> Make sure you have installed the python(3.10 and higher) and nodejs(v18.18.0 and higher)
##
Run next commands:
* ```git clone https://github.com/Leroy-bit/connect-four-online```
* ```cd server && pip install -r requirements.txt && cd ../client && npm install && npm run build```

## Running on local machine using ngrok
> it is assumed that you are already registered with ngrok and have your own static domain
```ngrok http --domain {your_ngrok_domain_name} 80```







