from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Classes.Post import Post
from Classes.Statistic import Statistic
from settings import *

class VkBot:

    def __init__(self):
        self.longpoll = longpoll
        self._COMMANDS = ["Выведи посты", "Рассчитать статистику", "Работа с историями"]
        self._COLORS = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                        VkKeyboardColor.SECONDARY]
        self.keyboard = self.spawnKeyboard()

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

    def spawnKeyboard(self):
        keyboard = VkKeyboard()
        for i in range(len(self._COMMANDS)):
            keyboard.add_button(label=self._COMMANDS[i], color=self._COLORS[i])
        return keyboard

    def postMsg(self, user_id):
        post = Post(user_id)
        attachment = post.checkPostsUser()
        likes = post.checkLikesUser()
        for i in range(0, len(attachment)):
            post.createPost(attachment[i])
            self.send_message(user_id, 'Пост набрал - ' + str(likes[i]['count']) + ' лайков')

    # Сообщение от пользователя
    def newMessage(self, request, user_id):
        try:
            if request == self._COMMANDS[0]:
                self.send_message(user_id, "Подождите немного...", self.keyboard)
                self.postMsg(user_id)
            elif request == self._COMMANDS[1]:
                stat = Statistic(user_id)
                stat.analyse_data()
                self.send_message(user_id, "Подождите немного....", self.keyboard)
                self.send_message(user_id, stat.strViewsStat)
                self.send_message(user_id, stat.strDataStat)
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
