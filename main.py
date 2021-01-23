import vk_api,json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from records_saver import save_top, load_top

bot_stone_records = 'data/stone_tops.txt'
from random import randint

key = "c4cf0a0661e38f87149ffdb72f81e97ef81fd4fec7c597d196bdc4e9a10291e328b0ea49cbd92693bd805"
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=key)


def send_message(user_id, message, file_vk_url=None, keyboard=None, car = None ):
    from random import randint
    vk.method('messages.send',
              {'user_id': user_id,
               "random_id": randint(1, 1000),
               'message': message,
               'attachment': file_vk_url,
               'keyboard': keyboard,
               'template':car,
               }
              )


def get_name(user_id, pad='Nom'):
    t = vk.method('users.get',
                  {'user_id': user_id,
                   'fields': ['bdate'],
                   'name_case': pad}
                  )
    t = t[0]
    print(t)
    if 'bday' in t:
        return (t['first_name'], t['last_name'], t['bday'])
    return (t['first_name'], t['last_name'], None)


def happy_early(user_id, text, ):
    about_user = vk.method('users.get', {'user_ids': user_id, 'fields': ' city, bdate,'})
    name_user = about_user[0].get('first_name')
    last_user = about_user[0].get('last_name')
    date_user = about_user[0].get('bdate')
    city = about_user[0].get('city').get('title')
    send_message(user_id,
                 'С отступающим старым новым годом и с наступающим новым новым годом!' + " " + name_user + " " + last_user + " " + date_user + " " + city)

    print(name_user)

carousel= {
    "type": "carousel",
    "elements": [{
            "photo_id": "-200628794_457239019",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки 🌚",
                    "payload": "{}"
                }
            }]
        },
        {
            "photo_id": "-109837093_457242811",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки 2",
                    "payload": "{}"
                }
            }]
        },
        {
            "photo_id": "-109837093_457242811",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки 3",
                    "payload": "{}"
                }
            }]
        }
    ]
}
carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
carousel = str(carousel.decode('utf-8'))


def game_01(user_id, text, fio):
    if text not in ['камень', 'ножницы', 'бумага', 'назад']:
        send_message(user_id, 'its a game,bro. press buttons', keyboard=game_keyboard)
    else:
        if text == 'назад':
            send_message(user_id, 'GG', keyboard=main_keyboard)
            wins = users[user_id]['wins']
            rounds = users[user_id]['round']
            ne_pobeda = rounds - wins
            if ((user_id not in top)
                    or
                    (wins - ne_pobeda > top[user_id])):
                top[user_id] = wins - ne_pobeda
                save_top(top, bot_stone_records)

            users[user_id] = {'status': 'main'}
        else:
            uspeh = randint(1, 3)
            if uspeh == 1:
                send_message(user_id, 'proigral')
            elif uspeh == 2:
                send_message(user_id, 'nich\'ya')
            elif uspeh == 3:
                send_message(user_id, 'выиграл')
                users[user_id]['wins'] += 1
            else:
                print(uspeh)
            users[user_id]['round'] += 1
            send_message(user_id, "побед" + str(users[user_id]['wins']) + '/' + str(users[user_id]['round']),
                         keyboard=game_keyboard)


def get_keyboard_x_y(x, y):
    keyboard = VkKeyboard(one_time=True)
    first = True
    for i in range(y):
        if not first:
            keyboard.add_line()  # Переход на вторую строку
        first = False
        for j in range(x):
            keyboard.add_button('y ' + str(i) + ',' + 'x ' + str(j))
    return keyboard.get_keyboard()


def generate_keyboard(variants, w=3):
    n = len(variants)
    x = w
    y = n // w
    if n % w:
        y += 1
    n_var = 0
    keyboard = VkKeyboard(one_time=True)
    first = True
    for i in range(y):
        if not first:
            keyboard.add_line()  # Переход на вторую строку
        first = False
        for j in range(x):
            if n_var < n:
                keyboard.add_button(variants[n_var], color=VkKeyboardColor.POSITIVE)
                n_var += 1
    return keyboard.get_keyboard()


main_keyboard = generate_keyboard(['об авторе', 'игра', 'тест', 'пинг'], w=3)
game_keyboard = generate_keyboard(['камень', 'ножницы', 'бумага', 'назад'], w=1)
back_keyboard = generate_keyboard(['назад'], w=1)
ping_keyboard = generate_keyboard(['назад', 'пинг'], w=1)
users = {}
top = load_top(bot_stone_records)
tanki_gamers = {}
while 1:
    try:

        # Работа с сообщениями
        longpoll = VkLongPoll(vk)
        # Основной цикл
        for event in longpoll.listen():
            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:
                    user_id = event.user_id
                    name, fam, bday = get_name(user_id)
                    text = event.text.lower()
                    if user_id not in users:
                        users[user_id] = {'status': 'main'}
                    if users[user_id]['status'] == 'main':
                        if text == 'об авторе':
                            send_message(user_id, 'Damir', keyboard=back_keyboard)
                        elif text == 'игра':
                            send_message(user_id, 'GAME', keyboard=game_keyboard)
                            users[user_id]['status'] = 'gaming_1'
                            users[user_id]['round'] = 0
                            users[user_id]['wins'] = 0
                        elif text == 'тест':
                            send_message(user_id, 'тесты близко, а готов ли ты, ' + name + " " + fam,
                                         keyboard=back_keyboard)
                        elif text == 'пинг':
                            send_message(user_id, 'понг', keyboard=ping_keyboard)
                        elif text == 'с новым годом':
                            happy_early(user_id, text, )
                        elif text == 'карусель':
                            send_message(user_id,'Apex this is top game for you')

                        else:
                            print(text)
                            print(text == 'c новым годом!')
                            send_message(user_id, 'Приветfed ' + name, keyboard=main_keyboard)

                    if users[user_id]['status'] == 'gaming_1':
                        game_01(user_id, text, [name, fam])
    except Exception as e:
        print(e)
    from time import sleep

    sleep(10)
