from settings import vk, vk_session


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = vk.method("users.get", {"user_ids": user_id})

    def getUserName(self):
        return self.user[0]['first_name'] + ' ' + self.user[0]['last_name']
    def getAveregeCountLikes(self):
        pass
    def getAveregeCountComments(self):
        pass
    def getAveregeCountReposts(self):
        pass
    def getCountFollowers(self):
        followers = vk_session.method('users.getFollowers', {'user_id': self.user_id, 'offset': 0})
        return followers["count"]
