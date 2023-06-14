import math
from settings import *
from Classes.Post import Post
from Classes.User import User

class Statistic:
    def __init__(self, user_id):
        self.id_text = None
        self.token = service_token
        self.version = version
        self.posts = Post(user_id)
        self.all_posts = self.posts.postObj
        self.subs = User(user_id).getCountFollowers()
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

    # Вычисление стандартного отклонения
    def std(self, x):
        std_result = 0
        mean = sum(x) / len(x)
        for a in x:
            std_result += (a - mean) ** 2 / (len(x) - 1)
        return math.sqrt(std_result)

    # Возвращает массив с оценкой вовлечённости для каждого поста
    def engagement_rate(self, x):
        rate = []
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(self.subs))])
        return rate

    # Вычисляет сумму массива по n элементу
    def summ(self,x, n):
        summ_m = 0
        for i in x:
            summ_m += i[n]
        return summ_m

    # Вычисляет значение ковариации
    def cov(self, x):
        cov_result = 0
        avg_x = self.summ(x, 0) / len(x)
        avg_y = self.summ(x, 1) / len(x)
        for i in range(len(x)):
            cov_result += (x[i][0] - avg_x) * (x[i][1] - avg_y)
        cov_result /= (len(x) - 1)
        return cov_result

    # Вычисляет значение коэфициента регрессионного анализа
    def regr_analys(self, x):
        r = self.cov(x) / (self.std([xi[1] for xi in x]) * self.std([yi[0] for yi in x]))
        return r

    # Анализирует данные
    def analyse_data(self):
        last_post_time_likes_delta = []
        self.likes_views = []
        self.likes_comm_reposts = []
        self.id_date = []
        self.id_text = []
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
                self.likes_views.append((self.all_posts["items"][i]['likes']['count'], 0))
                self.likes_comm_reposts.append((int(self.all_posts["items"][i]['id']), int(self.all_posts["items"][i]['likes']['count']),
                                                        int(self.all_posts["items"][i]['comments']['count']),
                                                        int(self.all_posts["items"][i]['reposts']['count'])))
                self.id_date.append([int(self.all_posts["items"][i]['id']), self.all_posts["items"][i]['date']])
            offset+=100
            print(self.id_date)
            self.posts.updatePostArr(offset)
            self.all_posts = self.posts.postObj
        rate_engagement = self.engagement_rate(self.likes_comm_reposts)

        if len(self.id_date) >= 4:
            for i in range(len(self.id_date) // 2 + 1):
                delta_date_post = self.id_date[i][1] - self.id_date[i + 1][1]
                delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
                last_post_time_likes_delta.append([delta_date_post, delta_rate_engagement_post])
        reg_analys_views = self.regr_analys(self.likes_views)
        reg_analys_date_delta = self.regr_analys(last_post_time_likes_delta)

        self.strViewsStat = ("Зависимость вовлечённости от просмотров - \n" + str(reg_analys_views))
        self.strDataStat = ("Зависимость вовлеченности от времени публикации между постами - \n" + str(reg_analys_date_delta))
        if(reg_analys_views > 0.7):
            self.strViewsStat += ".\nВовлеченность ваших подписчиков - хорошая"
        else:
            self.strViewsStat += ".\nВовлеченность ваших подписчиков - плохая"
        if (reg_analys_date_delta > 0.7):
            self.strDataStat += ".\nВы часто публикуете записи, ваши подписчики только рады)"
        else:
            self.strDataStat += ".\nОчень редко выставляете записи, я уже и сам не помню кто вы)"

