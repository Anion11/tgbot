from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from Classes.Post import Post
from settings import *
from fuzzywuzzy import fuzz


class VkBot:

    def __init__(self):
        self.longpoll = longpoll
        self._COMMANDS = ["ПРИВЕТ", "ПОКА", "ДАЙ ПОСТЫ", "НАЧАТЬ"]
        self._COLORS = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                        VkKeyboardColor.SECONDARY]

    # Метод для отправки сообщения пользователю
    def send_message(self, user_id, message, keyboard=None):
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": 0,
        }
        if keyboard is not None:
            post["keyboard"] = keyboard.get_keyboard()
        vk.method("messages.send", post)

    def spawnKeyboard(self, user_id):
        keyboard = VkKeyboard()
        for i in range(0, len(self._COMMANDS)//2):
            keyboard.add_button(label=self._COMMANDS[i], color=self._COLORS[i])
            self.send_message(user_id, self._COMMANDS[i], keyboard)
        keyboard.add_line()
        for i in range(len(self._COMMANDS) // 2, len(self._COMMANDS)):
            keyboard.add_button(label=self._COMMANDS[i], color=self._COLORS[i])
            self.send_message(user_id, self._COMMANDS[i], keyboard)


    def postMsg(self, user_id):
        post = Post(user_id)
        attachment = post.checkPostsUser()
        likes = post.checkLikesUser()
        for i in range(0, len(attachment)):
            post.createPost(attachment[i])
            self.send_message(user_id, 'Пост набрал - ' + str(likes[i]['count']) + ' лайков')

    # Сообщение от пользователя
    def newMessage(self, text, user_id):

        try:
            request = text
            if request.upper() == self._COMMANDS[0]:
                self.send_message(user_id, "Хай")
            elif request.upper() == self._COMMANDS[1]:
                self.send_message(user_id, "Пока((")
            elif request.upper() == self._COMMANDS[2]:
                self.send_message(user_id, "Подождите немного...")
                self.postMsg(user_id)
            elif request.upper() == self._COMMANDS[3]:
                self.spawnKeyboard(user_id)
            else:
                self.send_message(user_id, "Не понял вашего сообщения...")
            print('[log] 200: Успешно')
        except Exception as e:
            print(e)
            self.send_message(user_id, "Что то пошло не так...")
            self.send_message(user_id,
                              "Проверьте настройки приватности:\n1. Перейдите в раздел прочее\n2. Измените пункт "
                              "'Кому в интерете видна моя страница' на 'Всем'\n3. Если проблема не исчезла "
                              "напишите в поддержку (https://vk.com/iperelygin2015, https://vk.com/a1010101010)")
