import re

from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart

from filters import IsGroup
from loader import dp, db
from utils.pages.rating import page_rating
from utils.throttlig import rate_limit





@rate_limit(limit=3)
@dp.message_handler(Command('help'))
async def command_help(message: types.Message):
    text = f'❔<b>Как пользоваться ботом</b>❔\n\n' \
           f'Всё очень просто, напиши боту название книги и бот выдаст тебе все подходящие книги\n' \
           f'Либо ты можешь воспользоваться более точным поиском, с помощью следующих комманд: 👇\n\n' \
           f'/start - стартовая команда, чтобы впервые запустить бота\n' \
           f'/author <i>имя автора</i> - поиск только по авторам\n' \
           f'/series <i>название серии</i> - поиск только по названию серии\n' \
           f'/rating_b - показывает ТОП 10 книг по скачиваниям\n' \
           f'/rating_a - показывает ТОП 10 авторов по запросам\n' \
           f'/help - вызов справки, если ты забыл как пользоваться ботом🙃\n\n' \
           f'Примеры точных запросов:\n' \
           f'/author Джоан Роулинг\n' \
           f'/author Пушкин\n' \
           f'/series песнь льда и пламени\n' \
           f'/series Голодные Игры\n\n' \
           f'<b>P.S.</b>\n' \
           f'Книги доступны во всех форматах для скачивания\n' \
           f'Моя группа без ограничений: @free_book_flibusta\n' \
           f'Инструкция по созданию личной группы: /create_group'
    await message.answer(text)


@rate_limit(limit=3)
@dp.message_handler(CommandStart())
async def command_start(message: types.Message):

    text = f'Привет, {message.from_user.full_name}! \n\n' \
           f'Я помогу найти тебе любую книгу!😇\n' \
           f'Чтобы начать, пришли мне название книги 📖\n\n' \
           f'Я также могу производить поиск по ФИО автора или названию книжной серии ☺\n' \
           f'Ты можешь узнать больше обо мне здесь 👉 /help\n\n' \
           f'❗ ВАЖНАЯ ИНФОРМАЦИЯ ❗\n' \
           f'⚠Есть вероятность блокировки бота из-за нарушений прав правообладателей⚠\n' \
           f'Поэтому многие книги, авторы, книжные серии могут быть не доступны 😞\n\n' \
           f'<b>Бот работает без ограничений в группах</b>\n' \
           f'@free_book_flibusta - моя группа, где нет никаких ограничений\n' \
           f'Либо вы можете создать личную группу следуя инструкции: /create_group'

    await message.answer(text)
    await db.add_user(user=message.from_user.full_name, telegram_id=message.from_user.id)


@rate_limit(limit=3)
@dp.message_handler(Command('create_group'))
async def create_user_group(message: types.Message):
    text = '''
    ⚠ Существует большая вероятность блокировки бота за нарушение авторских прав ⚠
Чтобы пользоватся и дальше услугами бота, даже если он будет заблокирован 📵
Следуйте по инструкции ниже:\n

1. Инструкция:
- 1.1 создайте свою группу (инструкция по созданию на <a href="http://telegram.org.ru/374-kak-sozdat-gruppu-ili-kanal-v-telegram.html#hmenu-2">сайте телеграм</>)
- 1.2 добавьте в группу бота по [<a href="https://t.me/my_flibusta_bot?startgroup=1">этой ссылке</a>]
- 1.3 Перейдите в настройки группы и выберите пункт "Администраторы"
- 1.4 Нажмите добавить администратора и выберите бота \n
Готово! Можете продолжать поиски любимых книг 📚

Для Android можно скачать официальный клиент из <a href="http://telegram.org/android" >официального сайта</a> без авторских ограничений

    '''
    return await message.answer(text)


@rate_limit(limit=3)
@dp.message_handler(Command('rating_b'))
async def rating_top_book(message: types.Message):
    # Выводит топ 10 книг по скачиваниям
    rating_dict = await db.rating_top_10_values('book')
    descr = f'ТОП 10 КНИГ'
    text = page_rating(rating_dict, descr=descr)
    await message.answer(text)


@rate_limit(limit=3)
@dp.message_handler(Command('rating_a'))
async def rating_top_book(message: types.Message):
    # Выводит топ 10 авторов по запросам
    rating_dict = await db.rating_top_10_values('author')
    descr = f'ТОП 10 АВТОРОВ'
    text = page_rating(rating_dict, descr=descr)
    await message.answer(text)


@rate_limit(limit=3)
@dp.message_handler(regexp=re.compile(r'^/.+'))
async def other_command(message: types.Message):
    # Проверям на любую битую ссылку
    text = f'У меня нет такой комманды 😨\n' \
           f'Попробуй еще раз\n' \
           f'Либо можешь ознакомится со справкой 👉 /help'
    return await message.answer(text)
