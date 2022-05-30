from telebot.types import InputMediaPhoto
from telebot import types
from MenuBot import Menu
import requests
import telebot
import config
import random

bot = telebot.TeleBot(config.Telegram_TOKEN)


@bot.message_handler(commands=['start', 'restart'])
def start_message(message):
    text_message = f'Привет, {message.from_user.first_name}!\nВыбери желаемое действие.'
    bot.send_message(message.chat.id, text=text_message, reply_markup=Menu.get_menu('Главное меню').markup)


@bot.message_handler(content_types=['text'])
def get_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)
    if result is True:
        return

    if Menu.cur_menu is not None and ms_text in Menu.cur_menu.buttons:
        if ms_text == 'Помощь':
            help_button(message)

        elif ms_text == 'Рандомная игра':
            random_game(message)

    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")


def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu is not None and Menu.cur_menu.parent is not None:
        target_menu = Menu.get_menu(Menu.cur_menu.parent.name)

    else:
        target_menu = Menu.get_menu(name_menu)

    if target_menu is not None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        if target_menu.name == 'Развлечения':
            return True
    else:
        return False


def random_game(message):
    chat_id = message.chat.id
    id_data = [27, 34, 40, 41, 46, 53, 54, 73, 74, 76, 78, 79, 80, 81, 84, 86, 90, 96, 98, 101, 103, 105, 107, 111, 113,
               114, 115, 122, 123, 127, 129, 131, 132, 133, 135, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 150,
               151, 153, 155, 156, 158, 160, 162, 166, 170, 172, 174, 176, 178, 183, 191, 194, 197, 201, 208, 218, 219,
               223, 227, 228, 237, 245, 247, 252, 253, 263, 266, 283, 284, 285, 289, 294, 302, 318, 331, 338, 356, 359,
               360, 362, 363, 364, 366, 369, 372, 375, 377, 378, 379, 381, 382, 385, 387, 389, 390, 392, 393, 395, 396,
               397, 398, 400, 401, 403, 406, 408, 410, 413, 419, 420, 444, 478, 480, 481, 482, 483, 484, 485, 486, 487,
               488, 489, 491, 492, 493, 494, 495, 496]  # Пустые ID

    random_id = random.randint(1, 519)
    while random_id in id_data:
        random_id = random.randint(1, 519)

    req = requests.get(f'https://www.freetogame.com/api/game?id={random_id}')
    if req.status_code == 200:
        data = req.json()

        screenshot_1 = data['screenshots'][0]['image']
        screenshot_2 = data['screenshots'][1]['image']
        screenshot_3 = data['screenshots'][2]['image']
        release_date = data['release_date']
        description = data['description']
        publisher = data['publisher']
        developer = data['developer']
        game_url = data['game_url']
        platform = data['platform']
        poster = data['thumbnail']
        genre = data['genre']
        title = data['title']

        data_text = (f'*Название игры:* {title}\n'
                     f'*Жанр:* {genre}\n'
                     f'*Платформа:* {platform}\n'
                     f'*Дата релиза:* {release_date}\n'
                     f'*Разработчик:* {developer}\n'
                     f'*Издатель:* {publisher}\n')

        bot.send_message(chat_id, f'{data_text}\n'
                                  f'*Описание:* {description}[ ]({poster})', parse_mode='markdown')
        bot.send_media_group(chat_id, media=[InputMediaPhoto(screenshot_1), InputMediaPhoto(screenshot_2),
                                             InputMediaPhoto(screenshot_3)])
        bot.send_message(chat_id, text=f'*Ссылка на игру:* {game_url}', parse_mode='markdown')

    else:
        bot.send_message(chat_id, text='Ошибка соединения, попробуйте позже!')
        goto_menu(chat_id, 'Главное меню')


def help_button(message):
    bot.send_message(message.chat.id, "*Автор:* Полина Ивлева", parse_mode='markdown')
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Связаться с автором", url="https://t.me/LittleCommanderr")
    markup.add(btn)
    img = open('tyan.jpg', 'rb')
    bot.send_photo(message.chat.id, img, reply_markup=markup)


def dz(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('ТЫК', url='https://github.com/L1ttleCommander/TelegramBot/tree/main/DZ')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Ссылка на репозиторий:', reply_markup=markup)


bot.polling(none_stop=True, interval=0)
