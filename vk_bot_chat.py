import constans
import random
import datetime

import screen_full

from functools import wraps # многопоточность

import vk_api # подключения библиотек для работы вк бота
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

main_token = constans.token
from termcolor import colored #цветной текст

autorize = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(autorize, group_id=199663558)
upload = VkUpload(autorize)

now = datetime.datetime.now()

def mult_threading(func):
    """Декоратор для запуска функции в отдельном потоке"""
    @wraps(func)
    def wrapper(*args_, **kwargs_):
        import threading
        func_thread = threading.Thread(target=func,
                                       args=tuple(args_),
                                       kwargs=kwargs_)
        func_thread.start()
        return func_thread
    return wrapper

@mult_threading
def bot():
    def sender(chat_id):
        try:
            autorize.method("messages.send", {'chat_id': chat_id, "message": 'одну секунду!',
                                              "random_id": random.randint(1, 100)})
            attachments = []  # берем изображение
            upload_image = upload.photo_messages(photos=constans.image)[0]  # загружаем на сервер
            attachments.append(
                'photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))  # берем данные изображения
            autorize.method("messages.send",
                            {'chat_id': chat_id, "message": 'Держи!', "random_id": random.randint(1, 100),
                             'attachment': ','.join((attachments))})  # отправляем данные в чат
        except Exception:
            print(Exception)

    def update_screen(chat_id):
        print(colored("Новое сообщение о обновлении расписания", 'green'))
        autorize.method("messages.send",
                        {"chat_id": chat_id, "message": 'Происходит обновление, пожалуйста, подождите.',
                         "random_id": random.randint(1, 100)})
        screen_full.screen()
        sender(chat_id)

    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != "":
                request = event.message.get('text').lower()
                if request == "расписание":
                    print(colored("Написали в беседу под id:"+ str(event.chat_id) + " в " + str(now), 'green'))
                    sender(chat_id=event.chat_id);
                if request == "обновить расписание":
                    print(colored("Запрос на обновление в беседе под id:" + str(event.chat_id) + " в " + str(now), 'green'))
                    update_screen(chat_id=event.chat_id)
bot()