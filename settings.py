import vk_api
from vk_api.longpoll import VkLongPoll
from dotenv import load_dotenv
import os

load_dotenv()
# Токен сообщества
token = os.environ.get('TOKEN')
# Токен приложения
service_token = os.environ.get('SERVICE_TOKEN')
# id приложения
app_id = os.environ.get("APP_ID")
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
# Авторизуемся как приложение
vk_session = vk_api.VkApi(app_id=app_id, token=service_token)
# Работа с сообщениями
longpoll = VkLongPoll(vk)
