import vk_api
from vk_api.longpoll import VkLongPoll
# Токен сообщества
token = "vk1.a.gnP45oXmjfRQQ98cVi-O7CRwqlzv0QLwP6EEvaEwz9wy-C1OEhGlfJzqqo5msKA1YkDefbcBw3Bs1g2-q7VfA7tOGeDqRoXRGImPi27laWy3rJw6vbIAzOu9wW4-FCgz6z4AUWaBd1X-8iVZj-pCTJ-XXBaCDjawFt44YBdum2E6qZWJSC4DDnHgzGVriPnQzeQ4wkqYPc1YvcNyHf38RQ"
# Токен приложения
service_token = "a9092088a9092088a909208813aa1d55ceaa909a9092088cd8d7883b0a838f114762c25"
# id приложения
app_id = 51672390
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
# Авторизуемся как приложение
vk_session = vk_api.VkApi(app_id=app_id, token=service_token)
# Работа с сообщениями
longpoll = VkLongPoll(vk)