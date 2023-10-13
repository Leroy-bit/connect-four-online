from aiogram import Bot, Dispatcher, Router, types, filters
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
import config
import os
from base.entity import BaseEntity
import typing

if typing.TYPE_CHECKING:
    from base.application import Application
    from explorer import Explorer

class BotAccessor(BaseEntity):
    def setup(self) -> None:
        self.dp = Dispatcher()
        self.dp.startup.register(self.on_startup)
        self.bot = Bot(token=config.BOT_TOKEN, parse_mode='Markdown')
        webhook_handler = SimpleRequestHandler(self.dp, bot=self.bot, secret_token=config.WEBHOOK_SECRET_TOKEN)
        webhook_handler.register(self.explorer.app, path=config.WEBHOOK_PATH)
        setup_application(self.explorer.app, self.dp, bot=self.bot)
        self.register_handlers()
        return
    
    async def on_startup(self) -> None:
        await self.bot.set_webhook(config.BASE_URL + config.WEBHOOK_PATH, secret_token=config.WEBHOOK_SECRET_TOKEN)
        await self.bot.set_my_commands(self.register_bot_commands())
        return

    def register_handlers(self) -> None:
        router = Router()
        @router.message(filters.CommandStart())
        async def start(message: types.Message):
            await message.answer("To play click the button below, and select your friend to play with.", reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text='SELECT CHAT',
                            switch_inline_query_chosen_chat=types.SwitchInlineQueryChosenChat(allow_user_chats=True)
                        )
                    ]
                ]
            ))

        @router.message(filters.Command(commands=['help']))
        async def help(message: types.Message):
            await message.answer("This is bot to play the Connect Four game in Mini App. To start playing with friend send /start and follow instructions.")
        
        @router.inline_query()
        async def inline_query(query: types.InlineQuery):
            # return a Web App open URL
            me = await self.bot.me()
            await query.answer(
                results=[types.InlineQueryResultArticle(
                    id='start_game',
                    title='PLAY',
                    input_message_content=types.InputTextMessageContent(
                        message_text=f'[PLAY CONNECT FOUR](https://t.me/{me.username}/{config.MINI_APP_NAME}?game_id={query.from_user.id}',
                    ),
                    description='Start playing Connect Four',
                    thumbnail_url='https://telegra.ph/file/5bc2461d9ff7aee8c9929.png',
                    thumb_width=393,
                    thumbnail_height=393
                    )
                    ],
                cache_time=0
            )

        self.dp.include_router(router)
        return
    
    def register_bot_commands(self) -> None:
        return [
            types.BotCommand(command='/start', description='Start the bot'),
            types.BotCommand(command='/help', description='Get help'),
        ]

    def check_user_data(self, initData: str) -> WebAppInitData:
        try:
            data = safe_parse_webapp_init_data(config.BOT_TOKEN, initData)
            return data
        except ValueError:
            raise ValueError('wrong data from user')
        