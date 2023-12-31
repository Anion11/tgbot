from settings import vk, vk_session

class Post:

    def __init__(self, user_id):
        self.postObj = vk_session.method('wall.get', {'owner_id': user_id, 'offset': 0, 'count': 100})
        self.post_count = self.postObj['count']
        self.user_id = user_id

    def createPost(self,attachment, user_id):
        vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, "random_id": 0})

    def updatePostArr(self, offset):
        self.postObj = vk_session.method('wall.get', {'owner_id': self.user_id, 'offset': offset, 'count': 100})

    # Метод для подсчета количества лайков под постами
    def checkPostsUser(self, posts):
        attachmPosts = list()
        for i in range(0, len(posts)):
            attachmPosts.append('wall' + str(self.user_id) + "_" + str(posts[i]['id']))
        return attachmPosts

    def checkLikesUser(self):
        likes = list()
        for i in range(0, len(self.postObj['items'])):
            likes.append(vk_session.method('likes.getList',
                                          {'type': 'post', 'owner_id': self.user_id, 'item_id': self.postObj['items'][i]['id']}))
        return likes
