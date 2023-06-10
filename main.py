import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = "vk1.a.gnP45oXmjfRQQ98cVi-O7CRwqlzv0QLwP6EEvaEwz9wy-C1OEhGlfJzqqo5msKA1YkDefbcBw3Bs1g2-q7VfA7tOGeDqRoXRGImPi27laWy3rJw6vbIAzOu9wW4-FCgz6z4AUWaBd1X-8iVZj-pCTJ-XXBaCDjawFt44YBdum2E6qZWJSC4DDnHgzGVriPnQzeQ4wkqYPc1YvcNyHf38RQ"

serviceToken = "a9092088a9092088a909208813aa1d55ceaa909a9092088cd8d7883b0a838f114762c25"
app_id = 51672390
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vk_session = vk_api.VkApi(app_id=app_id, token=serviceToken)
def writeMsg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,"random_id":0})

def checkLiksUser(user_id):
    postObj = vk_session.method('wall.get', {'owner_id': user_id, 'offset': 0, 'count': 5})
    liks = list()
    for i in range(0,len(postObj['items'])):
        liks.append(vk_session.method('likes.getList', {'type': 'post', 'owner_id': user_id, 'item_id': postObj['items'][i]['id']}))
    for i in range(0,len(postObj['items'])):
        writeMsg(user_id,'Пост с id - ' + str(postObj['items'][i]['id']) + " набрал " + str(liks[i]['count']))

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
            elif request == "дай посты":
                checkLiksUser(event.user_id)
            else:
                writeMsg(event.user_id, "Не поняла вашего ответа...")