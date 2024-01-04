from aiogram import Bot, Dispatcher, Router, types, filters
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from aiogram.utils.i18n import I18n
import config
import os
from base.entity import BaseEntity
import typing

if typing.TYPE_CHECKING:
    from base.application import Application
    from explorer import Explorer

class BotAccessor(BaseEntity):
    '''Manages the telegram bot.'''

    def setup(self) -> None:
        self.dp = Dispatcher()
        self.i18n = I18n(path=os.path.join(config.BASE_DIR, 'server', 'locales'), default_locale='en', domain='messages')
        self._ = self.i18n.gettext
        self.dp.startup.register(self.onStartup)
        self.bot = Bot(token=config.BOT_TOKEN, parse_mode='Markdown')
        webhook_handler = SimpleRequestHandler(self.dp, bot=self.bot, secret_token=config.WEBHOOK_SECRET_TOKEN)
        webhook_handler.register(self.explorer.app, path=config.WEBHOOK_PATH)
        setup_application(self.explorer.app, self.dp, bot=self.bot)
        self.registerHandlers()
        
    async def setupBotCommands(self) -> list[types.BotCommand]:
        await self.bot.set_my_commands([
            types.BotCommand(command='/start', description='Start the bot'),
            types.BotCommand(command='/help', description='Get help'),
        ])

    async def onStartup(self) -> None:
        await self.bot.set_webhook(config.BASE_URL + config.WEBHOOK_PATH, secret_token=config.WEBHOOK_SECRET_TOKEN)
        await self.setupBotCommands()

    def registerHandlers(self) -> None:
        router = Router()

        @router.message(filters.CommandStart())
        async def start(message: types.Message) -> None:
            await self.explorer.db.handleUser(
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
                message.from_user.language_code)
            await message.answer(
                self._(
                    'To play click the button below, and select chat in which you want to play.', 
                    locale=message.from_user.language_code
                ), 
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text=self._('Select Chat', locale=message.from_user.language_code),
                                switch_inline_query_chosen_chat=types.SwitchInlineQueryChosenChat(allow_user_chats=True)
                            )
                        ]
                    ]
                )
            )

        @router.message(filters.Command(commands=['help']))
        async def help(message: types.Message) -> None:
            await message.answer(
                self._(
                    'This is a bot created to play the Connect Four game in Mini App. To start playing with friend send /start and follow instructions.', 
                    locale=message.from_user.language_code
                )
            )
        
        @router.inline_query()
        async def inline_query(query: types.InlineQuery) -> None:
            # return a Web App open URL
            me = await self.bot.me()
            await query.answer(
                results=[types.InlineQueryResultArticle(
                    id='start_game',
                    title=self._('Play', locale=query.from_user.language_code),
                    input_message_content=types.InputTextMessageContent(
                        message_text=f'[{self._("Play Connect Four", locale=query.from_user.language_code)}](https://t.me/{me.username}/{config.MINI_APP_NAME}?game_id={query.from_user.id}',
                    ),
                    description=self._('Start playing Connect Four', locale=query.from_user.language_code),
                    thumbnail_url='https://telegra.ph/file/5bc2461d9ff7aee8c9929.png',
                    thumb_width=393,
                    thumbnail_height=393
                    )
                    ],
                cache_time=0
            )

        self.dp.include_router(router)

    async def checkUserData(self, initData: str) -> WebAppInitData:
        try:
            data = safe_parse_webapp_init_data(config.BOT_TOKEN, initData)
            return data
        except ValueError:
            raise ValueError('wrong data from user')
        