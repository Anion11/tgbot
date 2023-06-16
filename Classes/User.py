from settings import vk, vk_session


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = vk.method("users.get", {"user_ids": user_id, "fields": "domain"})
        self.user_domain = self.user[0]["domain"]
    #получить имя и фамилию пользователя
    def getUserName(self):
        return self.user[0]['first_name'] + ' ' + self.user[0]['last_name']
