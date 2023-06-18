from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Classes.Groups import Groups
from Classes.Post import Post
from Classes.Statistic import Statistic
from Classes.User import User
from settings import *
import re

class VkBot:

    def __init__(self):
        self.longpoll = longpoll
        self._COMMANDS_USER = ["Рассчитать статистику страницы", "Вывести посты со статистикой страницы", "Работа с группой"]
        self._COMMANDS_GROUP = ["Рассчитать статистику группы", "Вывести посты со статистикой группы", "Работа с моей страницей", "https://vk.com/"]
        self._COLORS = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                        VkKeyboardColor.SECONDARY]
        self.keyboard = self.spawnKeyboardUser()
        self.groups = Groups()
        self.user_id = None
        self.user = None
        self.dateTimePattern = [re.compile("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"), re.compile("^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$"),
                        re.compile("^[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}$")]

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

    def setUserId(self, user_id):
        self.user_id = user_id
        self.user = User(user_id)
    def spawnKeyboardUser(self):
        keyboard = VkKeyboard()
        for i in range(len(self._COMMANDS_USER)):
            keyboard.add_button(label=self._COMMANDS_USER[i], color=self._COLORS[i])
        return keyboard
    def spawnKeyboardGroup(self):
        keyboard = VkKeyboard()
        for i in range(len(self._COMMANDS_GROUP) - 1):
            keyboard.add_button(label=self._COMMANDS_GROUP[i], color=self._COLORS[i])
        return keyboard

    def postMsg(self, user):
        post = Post(user)
        stat = Statistic(self.user.user_domain, "01.01.2000")
        attachment = post.checkPostsUser()
        likes = post.checkLikesUser()
        for i in range(0, len(attachment)):
            post.createPost(attachment[i],self.user_id)
            er_post = stat.check_engagement_rate_post(post.postObj['items'][i]['id'])
            self.send_message(self.user_id, str(er_post))
    def allAnalys(self, stat):
        result = stat.print_analyse()
        if result != -1:
            self.send_message(self.user_id, stat.strVovlDate)
            self.send_message(self.user_id, stat.strVovlOtm)
            self.send_message(self.user_id, stat.strVovlViews)
            self.send_message(self.user_id, stat.timeToVideo)
            self.send_message(self.user_id, stat.timeToPhoto)
        else:
            self.send_message(self.user_id, "Слишком мало постов, невозможно рассчитать статистику")
    # Сообщение от пользователя
    def newMessage(self, request):
        try:
            if request == self._COMMANDS_USER[1]:
                self.send_message(self.user_id, "Подождите немного...", self.keyboard)
                self.postMsg(self.user_id)
            elif request == self._COMMANDS_GROUP[1]:
                if (self.groups.have_domain):
                    self.send_message(self.user_id, "Подождите немного...", self.keyboard)
                    self.postMsg(self.groups.group_id)
                else:
                    self.send_message(self.user_id, "Пришлите ссылку на вашу группу", self.keyboard)
            elif request == self._COMMANDS_USER[0] or request == self._COMMANDS_GROUP[0]:
                self.send_message(self.user_id, "Введите начальную дату рассчета в формате дд.мм.гггг")
            elif (re.fullmatch(self.dateTimePattern[0], request) or re.fullmatch(self.dateTimePattern[1], request)
                   or re.fullmatch(self.dateTimePattern[2], request)):
                self.send_message(self.user_id, "Подождите немного...", self.keyboard)
                if (self.groups.have_domain):
                    stat = Statistic(self.groups.domain, request)
                    self.allAnalys(stat)
                else:
                    stat = Statistic(self.user.user_domain, request)
                    self.allAnalys(stat)
            elif request == self._COMMANDS_USER[2]:
                self.keyboard = self.spawnKeyboardGroup()
                self.send_message(self.user_id, "Вы перешли на режим работы с группой", self.keyboard)
                self.send_message(self.user_id, "Пришлите ссылку на вашу группу", self.keyboard)
            elif request == self._COMMANDS_GROUP[2]:
                self.keyboard = self.spawnKeyboardUser()
                self.send_message(self.user_id, "Вы перешли на режим работы со своей страницей", self.keyboard)

            elif self._COMMANDS_GROUP[3] in request:
                domain = request.partition(self._COMMANDS_GROUP[3])[2]
                self.groups.initDomain(domain)
                self.send_message(self.user_id, "Группа сохранена")
            else:
                self.send_message(self.user_id, "Не поняла вашего сообщения... Повторите попытку")
            print('[log] 200: Успешно')
        except Exception as e:
            print(f"[log] {e}")
            self.send_message(self.user_id, "Что то пошло не так...")
            self.send_message(self.user_id,
                              "Проверьте настройки приватности:\n1. Перейдите в раздел прочее\n2. Измените пункт "
                              "'Кому в интерете видна моя страница' на 'Всем'\n3. Если проблема не исчезла "
                              "напишите в поддержку (https://vk.com/iperelygin2015, https://vk.com/a1010101010)")