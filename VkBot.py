import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange, random
from youtubesearchpython import *
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

#доступные команды
commands = {
    '/название' : 'title',
    '/дата' : 'publishedTime',
    '/длительность' : 'duration',
    '/просмотры' : 'viewCount',
    '/автор' : 'channel',
    '/инфо' : 'accessibility'
}


def get_result(video_link, data): #однократное исполнение команд
    #исключения для более развернутых ответов
    if data == 'viewCount':
        result = video_link.result()['result'][0][data]['short']
    elif data == 'channel':
        result = video_link.result()['result'][0][data]['name']
    elif data == 'accessibility':
        result = video_link.result()['result'][0][data]['title']
    else:
        #единый способ исполнения команды
        result = video_link.result()['result'][0][data]
    return result  #возращение результата после команды

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
        if event.from_user and (event.text).lower() not in commands: #поиск видео
            link = VideosSearch(event.text,limit=1)
            vk.messages.send(user_id=event.user_id,
                             message=get_result(video_link=link, data='link'),
                             random_id = randrange(0,10000))
                            #результат поиска
        elif event.from_user and (event.text).lower() in commands: #контекст исполнение команд
            vk.messages.send(user_id=event.user_id,
                             message=get_result(
                                 video_link=link,
                                 data=commands[(event.text).lower()]),
                             random_id=randrange(0,10000))