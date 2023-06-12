# Импортируем библиотеки
from datetime import timedelta
from Classes.User import User
from engine import VkBot
from vk_api.longpoll import VkEventType
#создаем экземпляр бота
bot = VkBot()

print("[log] Бот запущен")
# Основной цикл
for event in bot.longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            user = User(event.user_id)
            print(" ")
            print(f"[log] Новое сообщение: {event.text}")
            print(f"[log] Отправитель: {user.getUserName()}")
            print(f"[log] Дата: {(event.datetime + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}")
            bot.newMessage(event.text, user.user_id)