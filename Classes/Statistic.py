import datetime
from settings import *
from Classes.Post import Post
from Classes.User import User
from Classes.Utils import Utils

class Statistic:
    def __init__(self, user_id):
        self.subs = User(user_id).getCountFollowers()
        self.token = service_token
        self.version = version
        self.posts = Post(user_id)
        self.all_posts = self.posts.postObj
        self.best_choice = []
        self.user_id = user_id
        self.strViewsStat = None
        self.strDataStat = None
    # Возвращает массив, где выведенео количество упоминаний в посте
    def check_count_id(self):
        count_id = []
        for text in self.id_text:
            if text is not None:
                count_id.append(text[1].count("id"))
            else:
                count_id.append(0)
        return count_id
     # Возвращает массив с оценкой вовлечённости для каждого поста
    def engagement_rate(self):
        rate = []
        x = self.likes_comm_reposts
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(self.subs))])
        return rate
    # Инициализация всех нужных массивов данных
    def init_all_posts(self):
        self.likes_views = []
        self.likes_comm_reposts = []
        self.id_date = []
        self.id_text = []
        self.id_type = []
        offset = 0
        ok = False
        while offset < 500 and not ok:
            if self.all_posts['items'] == [] or (offset > 0 and int(self.all_posts["items"][0]["id"]) == self.id_date[0][0]):
                ok = True
            for i in range(len(self.all_posts["items"])):
                try:
                    self.likes_views.append((self.all_posts["items"][i]['likes']['count'], self.all_posts["items"][i]['views']['count']))
                except:
                    self.likes_views.append((self.all_posts["items"][i]['likes']['count'], 0))
                self.likes_comm_reposts.append((int(self.all_posts["items"][i]['id']), int(self.all_posts["items"][i]['likes']['count']),
                                                        int(self.all_posts["items"][i]['comments']['count']),
                                                        int(self.all_posts["items"][i]['reposts']['count'])))
                self.id_date.append([int(self.all_posts["items"][i]['id']), self.all_posts["items"][i]['date']])
                self.id_text.append([self.all_posts["items"][i]['id'], self.all_posts["items"][i]['text']])
                try:
                    self.id_type.append([self.all_posts["items"][i]['id'], self.all_posts["items"][i]['attachments'][0]["type"],
                                               self.all_posts["items"][i]['date']])
                except:
                    pass
            offset+=100
            self.posts.updatePostArr(offset)
            self.all_posts = self.posts.postObj
        self.last_post_time_likes_delta = []
        rate_engagement = self.engagement_rate()

        if len(self.id_date) >= 4:
            for i in range(len(self.id_date) // 2 + 1):
                delta_date_post = self.id_date[i][1] - self.id_date[i + 1][1]
                delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
                self.last_post_time_likes_delta.append([delta_date_post, delta_rate_engagement_post])
    def optimal_time_post(self):
        def time_matrix():
            print("work __time_matrix")
            self.best_choice = []
            sr_0810 = []
            sr_1012 = []
            sr_1214 = []
            sr_1416 = []
            sr_1618 = []
            sr_1820 = []
            sr_2008 = []
            rate = self.engagement_rate()
            for i in range(len(self.id_type)):
                time_post = int(datetime.datetime.fromtimestamp(self.id_type[i][2]).strftime("%H"))
                if 8 <= time_post <= 10:
                    sr_0810 += [['0810', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                if 10 < time_post <= 12:
                    sr_1012 += [['1012', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                if 12 < time_post <= 14:
                    sr_1214 += [['1214', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                if 14 < time_post <= 16:
                    sr_1416 += [['1416', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                if 16 < time_post <= 18:
                    sr_1618 += [['1618', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                if 18 < time_post <= 20:
                    sr_1820 += [['1820', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]
                else:
                    sr_2008 += [['2008', self.id_type[i][0], self.id_type[i][1], self.id_type[i][2], rate[i][0]]]

            best_type(sr_0810)
            best_type(sr_1012)
            best_type(sr_1214)
            best_type(sr_1416)
            best_type(sr_1618)
            best_type(sr_1820)
            best_type(sr_2008)

        def best_type(sr_time):
            photos = []
            videos = []
            photos_rate = 0
            videos_rate = 0
            if len(sr_time) != 0:
                for i in range(len(sr_time)):
                    if sr_time[i][2] == 'photo':
                        photos.append(sr_time[i][4])
                    if sr_time[i][2] == 'video':
                        videos.append(sr_time[i][4])
                if len(photos) != 0:
                    photos_rate = sum(photos) / int(len(photos))
                if len(videos) != 0:
                    videos_rate = sum(videos) / int(len(videos))
                if photos_rate > videos_rate:
                    self.best_choice.append([sr_time[0][0], photos_rate, 'photos'])
                if photos_rate < videos_rate:
                    self.best_choice.append([sr_time[0][0], videos_rate, 'videos'])
        print("work __optimal_time_post")
        
        time_matrix()
        
        matrix = self.best_choice
        index_max_stat_time_photo = -1
        index_max_stat_time_video = -1
        max_ph = 0
        max_vid = 0
        k = 0
        for i in matrix:
            if i[2] == 'photos' and i[1] > max_ph:
                max_ph = i[1]
                index_max_stat_time_photo = k
            if i[2] == 'videos' and i[1] > max_vid:
                max_vid = i[1]
                index_max_stat_time_video = k
            k += 1
        if index_max_stat_time_photo != -1:
            time_ph = matrix[index_max_stat_time_photo][0][0:2] + ':00 - ' + matrix[index_max_stat_time_photo][0][
                                                                            2:4] + ':00' + ": " + \
                    matrix[index_max_stat_time_photo][2]
            print(time_ph)
        if index_max_stat_time_video != -1:
            time_vid = matrix[index_max_stat_time_video][0][0:2] + ':00 - ' + matrix[index_max_stat_time_video][0][
                                                                            2:4] + ':00' + ": " + \
                    matrix[index_max_stat_time_video][2]
            print(time_vid)
        
    
    # Анализирует данные
    def analyse_data(self):
        self.init_all_posts()
        
        reg_analys_views = Utils.regr_analys(Utils, self.likes_views)
        reg_analys_date_delta = Utils.regr_analys(Utils, self.last_post_time_likes_delta)
        self.optimal_time_post()
        self.strViewsStat = ("Зависимость вовлечённости от просмотров = \n" + str(reg_analys_views))
        self.strDataStat = ("Зависимость вовлеченности от времени публикации между постами = \n" + str(reg_analys_date_delta))
        if(reg_analys_views > 0.7):
            self.strViewsStat += ".\nВовлеченность ваших подписчиков - хорошая"
        else:
            self.strViewsStat += ".\nВовлеченность ваших подписчиков - плохая"
        if (reg_analys_date_delta > 0.7):
            self.strDataStat += ".\nВы часто публикуете записи, ваши подписчики только рады)"
        else:
            self.strDataStat += ".\nОчень редко выставляете записи, я уже и сам не помню кто вы)"