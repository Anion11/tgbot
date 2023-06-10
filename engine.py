from settings import *
from fuzzywuzzy import fuzz
class VkBot:

    def __init__(self):
        self.longpoll = longpoll
        self._COMMANDS = ["ПРИВЕТ", "ДАЙ ПОСТЫ", "ПОКА"]

    # Метод для отправки сообщения пользователю
    def writeMsg(self, user_id, message):
        vk.method('messages.send', {'user_id': user_id, 'message': message,"random_id":0})
    # Метод для подсчета количества лайков под постами
    def checkLikesUser(self, user_id):
        postObj = vk_session.method('wall.get', {'owner_id': user_id, 'offset': 0, 'count': 5})
        liks = list()
        for i in range(0,len(postObj['items'])):
            liks.append(vk_session.method('likes.getList', {'type': 'post', 'owner_id': user_id, 'item_id': postObj['items'][i]['id']}))
        for i in range(0,len(postObj['items'])):
            self.writeMsg(user_id,'Пост с id - ' + str(postObj['items'][i]['id']) + " набрал " + str(liks[i]['count']))
    def getTime(self):
        return vk.method('utils.getServerTime')
    def getUserName(self, event):
            user = vk.method("users.get", {"user_ids": event.user_id}) 
            return user[0]['first_name'] +  ' ' + user[0]['last_name']
    # Сообщение от пользователя
    def newMessage(self, event):
        try:
            user_id = event.user_id
            request = self.fuzzyСomparison(event.text)
            if request.upper() == self._COMMANDS[0]:
                self.writeMsg(user_id, "Хай")
            elif request.upper() == self._COMMANDS[2]:
                self.writeMsg(user_id, "Пока((")
            elif request.upper() == self._COMMANDS[1]:
                self.writeMsg(user_id, "Подождите немного...")
                self.checkLikesUser(user_id)
            else:
                self.writeMsg(user_id, "Не понял вашего сообщения...")
        except Exception as e:
            print("Что то пошло не так...")
            self.writeMsg(user_id, "Что то пошло не так...")
    def fuzzyСomparison(self, text): #нечеткое распознование
        for c in self._COMMANDS:
            vrt = fuzz.ratio(text.upper(), c.upper())
            if vrt > 85:
                return c
        return ""
        