# Импортируем библиотеки
from datetime import datetime
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
            print(" ")
            print(f"[log] Новое сообщение: {event.text}")
            print(f"[log] Отправитель: {bot.getUserName(event)}")
            print(f"[log] Дата: {datetime.utcfromtimestamp(bot.getTime()).strftime('%Y-%m-%d %H:%M:%S')}")
            bot.newMessage(event)