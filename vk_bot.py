from time import time, sleep
import datetime
import random # библиотека рандома

import constans
import vk_bot_chat #работа вк чата
import screen_full # подлючения файла с кодом скриншота
import unittest #работа скриншота страницы сайта

from functools import wraps # многопоточность

import vk_api# для работы вк бота
from vk_api import VkUpload# для работы вк бота
from vk_api.longpoll import VkLongPoll, VkEventType # для работы вк бота

from termcolor import colored #цветной текст

main_token = constans.token

vk_session = vk_api.VkApi(token = main_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)

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


def message_console(): # сообщения в консоль
    print(colored("Работа началась в " + str(now), 'red'))

@mult_threading
def screen_repeat(sleeps):# скриншот с сайта повторяющийся
    while True:
        sleep(sleeps) # время, через которое будет запускаться новый скрин
        screen_full.screen()
        print(colored("Обновлено расписание в " + str(now),'red'))

@mult_threading
def job_bot(): # работа бота вк
    def full_name_users(user_id): # получение полного имени пользователя
        vk_user = vk.users.get(user_id=user_id)
        user_get = vk_user[0]
        first_name = user_get['first_name']
        last_name = user_get['last_name']
        full_name = first_name + " " + last_name
        return full_name

    def write_msg_photo():  # функция отправки сообщения с картинкой расписания
        print("Новое сообщение в лс от " + full_name_users(event.user_id) + " в " + str(now))
        try:
            vk_session.method("messages.send", {"user_id":event.user_id, "message": 'одну секунду!',
                                            "random_id": random.randint(1, 100)})
            attachments = []  # берем изоражение
            upload_image = upload.photo_messages(photos=constans.image)[0]  # загружаем на сервер
            attachments.append(
                'photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))  # берем данные изображения
            vk_session.method("messages.send",
                              {"user_id":event.user_id, "message": 'Держи!', "random_id": random.randint(1, 100),
                               'attachment': ','.join((attachments))}) # отправляем данные в чат
            print("Отправлено расписание в " + str(now) + " для " + full_name_users(event.user_id))
        except Exception:
            print(Exception)

    def update_screen():
        print("Новое сообщение о обновлении расписания")
        vk_session.method("messages.send", {"user_id":event.user_id, "message": 'Происходит обновление, пожалуйста, подождите.',
                                            "random_id": random.randint(1, 100)})
        screen_full.screen()
        write_msg_photo()

    while True:
        try:
            for event in longpoll.listen(): # читаем сообщения
                if event.type == VkEventType.MESSAGE_NEW: # если есть новые, то отвечаем
                    if event.from_user:
                        request = event.text.lower()
                        if request == "расписание":
                            write_msg_photo()
                        if request == "обновить расписание":
                            update_screen()
        except Exception:
            print(Exception)

message_console()
job_bot()
screen_repeat(3600)