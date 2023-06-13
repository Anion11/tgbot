import time
import math
import requests
from settings import *
from Post import Post

class Logic:
    def __init__(self, user_id):
        self.id_likes_type = None
        self.id_text = None
        self.id_date = None
        self.likes_comm_reposts = None
        self.likes_views = None
        self.x = None
        self.token = service_token
        self.version = version
        self.all_posts = Post().postObj
        self.user_id = user_id

    # Возвращает количество подписчиков
    def get_count_subs(self):
            response_subs = requests.get("https://api.vk.com/method/users.getFollowers",
                                         params=
                                         {"user_id": self.user_id,
                                          "access_token": self.token,
                                          "v": self.version
                                          }
                                         )
            time.sleep(1)
            return response_subs.json()['response']['count']
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
        subs = self.get_count_subs()
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(subs))])
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

        rate_engagement = self.engagement_rate(self.likes_comm_reposts)

        count_id = self.check_count_id()
        count_id_rate = []

        for i in range(len(count_id)):
            count_id_rate.append([count_id[i], rate_engagement[i][0]])

        for i in range(len(self.id_date) // 2 + 1):
            delta_date_post = self.id_date[i][1] - self.id_date[i + 1][1]
            delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
            last_post_time_likes_delta.append([delta_date_post, delta_rate_engagement_post])

        regr_analys_id = self.regr_analys(count_id_rate)
        reg_analys_views = self.regr_analys(self.likes_views)
        reg_analys_date_delta = self.regr_analys(last_post_time_likes_delta)

        print("Зависимость вовлечённости от просмотров - ", reg_analys_views)
        print("Зависимость вовлеченности от времени публикации между постами - ", reg_analys_date_delta)
        print("Зависимость вовлеченности от использованных отметок ", regr_analys_id)
        return reg_analys_views, reg_analys_date_delta, regr_analys_id