from aiogram import executor
from loader import dp


async def on_startup(dispatcher):
    import middlewares, handlers
    from utils.set_bot_command import set_default_commands

    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
