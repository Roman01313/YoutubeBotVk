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
            link = VideosSearch(event.text, limit=1).result()['result'][0]['link']
            vk.messages.send(user_id=event.user_id, message=f'Найдено по вашему запросу :{link}', random_id=randrange(1,10000))
