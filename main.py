import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def writeMsg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,"random_id":0})
    
# API-ключ созданный ранее
token = "vk1.a.gnP45oXmjfRQQ98cVi-O7CRwqlzv0QLwP6EEvaEwz9wy-C1OEhGlfJzqqo5msKA1YkDefbcBw3Bs1g2-q7VfA7tOGeDqRoXRGImPi27laWy3rJw6vbIAzOu9wW4-FCgz6z4AUWaBd1X-8iVZj-pCTJ-XXBaCDjawFt44YBdum2E6qZWJSC4DDnHgzGVriPnQzeQ4wkqYPc1YvcNyHf38RQ"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
    
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
        
            # Сообщение от пользователя
            request = event.text
            print(event.user_id)
            print(request)
            # Каменная логика ответа
            if request == "привет":
                writeMsg(event.user_id, "Хай")
                
            elif request == "пока":
                writeMsg(event.user_id, "Пока((")
            else:
                writeMsg(event.user_id, "Не поняла вашего ответа...")