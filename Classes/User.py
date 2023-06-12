from settings import vk


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = vk.method("users.get", {"user_ids": user_id})

    def getUserName(self):
        return self.user[0]['first_name'] + ' ' + self.user[0]['last_name']

    def getAveregeCountLikes():
        pass

    def getAveregeCountComments():
        pass

    def getAveregeCountReposts():
        pass
