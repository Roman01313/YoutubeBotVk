import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from youtubesearchpython import *
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
        if event.from_user:
            link = VideosSearch(event.text, limit=3)
            print(link.result())
            for i in range(len(link.result()['result'])):
                vid = link.result()['result'][i]['link']
                tit = link.result()['result'][i]['title']
                creator = link.result()['result'][i]['channel']['name']
                publish_time = link.result()['result'][i]['publishedTime']
                duration = link.result()['result'][i]['duration']
                views = link.result()['result'][i]['viewCount']['short']
                vk.messages.send(user_id=event.user_id, message=f'Автор:{creator}\n'
                                                                f'Название:{tit}\n'
                                                                f'Найдено по вашему запросу :{vid}\n'
                                                                f'Дата публикации: {publish_time}\n'
                                                                f'Длительность: {duration}\n'
                                                                f'Кол-во просмотров:{views}\n',
                                 random_id=randrange(1,10000))