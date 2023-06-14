import datetime
import time

import math
import requests


class Logic:
    def __init__(self, token, version, domain):
        self.delta_date_post = None
        self.id_likes_type = None
        self.id_text = None
        self.id_date = None
        self.likes_comm_reposts = None
        self.likes_views = None
        self.x = None
        self.token = token
        self.version = version
        self.domain = domain
        self.all_posts = []

    # Получение id пользователя
    def get_id(self):
        response_subs = requests.get("https://api.vk.com/method/utils.resolveScreenName",
                                     params=
                                     {
                                         "screen_name": self.domain,
                                         "access_token": self.token,
                                         "v": self.version
                                     }
                                     )
        options = [response_subs.json()['response']['type'], response_subs.json()['response']['object_id']]
        return options

    # Возвращает количество подписчиков
    def get_count_subs(self):
        subs_type = self.get_id()
        try:
            if subs_type[0] == 'group':
                response_subs = requests.get("https://api.vk.com/method/groups.getMembers",
                                             params=
                                             {"group_id": subs_type[1],
                                              "access_token": self.token,
                                              "v": self.version
                                              }
                                             )
                time.sleep(1)
                return response_subs.json()['response']['count']
            if subs_type[0] == 'user':
                response_subs = requests.get("https://api.vk.com/method/users.getFollowers",
                                             params=
                                             {"user_id": subs_type[1],
                                              "access_token": self.token,
                                              "v": self.version
                                              }
                                             )
                time.sleep(1)
                sub = response_subs.json()['response']['count']

                response_friend = requests.get("https://api.vk.com/method/friends.get",
                                               params=
                                               {"user_id": subs_type[1],
                                                "fields": self.domain,
                                                "access_token": self.token,
                                                "v": self.version
                                                }
                                               )
                friend = response_friend.json()['response']['count']
                subs = sub = friend
                return subs
        except:
            print("Ошибка чтения кол-ва подписчиков\n Укажите число ваших подписчиков:")
            subs = int(input())
            return subs

    # Возвращает массив, где выведенео количество упоминаний в посте
    def check_count_id(self):
        count_id = []
        for text in self.id_text:
            if text is not None:
                count_id.append(text[1].count("id"))
            else:
                count_id.append(0)
        return count_id

    def get_posts(self):
        offset = 0
        count = 100

        while offset < 1000:
            response = requests.get("https://api.vk.com/method/wall.get",
                                    params=
                                    {
                                        "access_token": self.token,
                                        "v": self.version,
                                        "domain": self.domain,
                                        "count": count,
                                        "offset": offset
                                    }
                                    )
            data = response.json()['response']['items']
            offset += 100
            self.all_posts.extend(data)
            time.sleep(0.1)

            self.likes_views = []
            self.likes_comm_reposts = []
            self.id_date = []
            self.id_text = []
            self.id_likes_type = []
            for i in range(len(self.all_posts)):
                if self.all_posts[i]['from_id'] == self.get_id()[1]:
                    try:
                        self.likes_views.append(
                            (self.all_posts[i]['likes']['count'], self.all_posts[i]['views']['count']))
                        self.likes_comm_reposts.append(
                            (int(self.all_posts[i]['id']), int(self.all_posts[i]['likes']['count']),
                             int(self.all_posts[i]['comments']['count']),
                             int(self.all_posts[i]['reposts']['count'])))
                        self.id_date.append([self.all_posts[i]['id'], self.all_posts[i]['date']])
                        self.id_text.append([self.all_posts[i]['id'], self.all_posts[i]['text']])
                        self.id_likes_type.append([self.all_posts[i]['id'], self.all_posts[i]['likes']['count']])
                    except Exception as ex:
                        ex = ex

            return self.all_posts

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
    def summ(self, x, n):
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
        global regr_analys_id
        self.get_posts()

        last_post_time_likes_delta = []

        rate_engagement = self.engagement_rate(self.likes_comm_reposts)

        count_id = self.check_count_id()
        count_id_rate = []

        if sum(count_id_rate) > 0:
            for i in range(len(count_id)):
                count_id_rate.append([count_id[i], rate_engagement[i][0]])
        for i in range(len(self.id_date) // 2 + 1):
            self.delta_date_post = self.id_date[i][1] - self.id_date[i + 1][1]
            delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
            last_post_time_likes_delta.append([self.delta_date_post, delta_rate_engagement_post])
        if sum(count_id_rate) > 0:
            regr_analys_id = self.regr_analys(count_id_rate)
        else:
            regr_analys_id = 0
        reg_analys_views = self.regr_analys(self.likes_views)
        reg_analys_date_delta = self.regr_analys(last_post_time_likes_delta)
        return reg_analys_views, reg_analys_date_delta, regr_analys_id

    def print_analyse(self):
        reg_analys_views, reg_analys_date_delta, regr_analys_id = self.analyse_data()
        print("Зависимость вовлечённости от просмотров - ", round(reg_analys_views, 2))
        print("Зависимость вовлеченности от времени публикации между постами - ", reg_analys_date_delta)
        print("Зависимость вовлеченности от использованных отметок ", regr_analys_id)


token = '4ac322d84ac322d84ac322d8e949d758f444ac34ac322d82e456929d7964209057d8233'
version = 5.131
domain = "a1010101010"

user = Logic(token, version, domain)
user.print_analyse()
print("")
