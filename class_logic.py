import datetime
import time
import data_analys
import math
import requests


class Logic:
    def __init__(self, token, version, domain, date):
        self.__id_type = []
        self.__delta_date_post = []
        self.__id_text = []
        self.__id_date = []
        self.__likes_comm_reposts = []
        self.__likes_views = []
        self.__best_choice = []
        self.__token = token
        self.__version = version
        self.__domain = domain
        self.__all_posts = []
        self.__photos_all = []
        self.__videos_all = []
        self.__all_posts_respone = []
        self.__enter_date = date

    # Получение id пользователя
    def get_id(self):
        response_subs = requests.get("https://api.vk.com/method/utils.resolveScreenName",
                                     params=
                                     {
                                         "screen_name": self.__domain,
                                         "access_token": self.__token,
                                         "v": self.__version
                                     }
                                     )
        options = [response_subs.json()['response']['type'], response_subs.json()['response']['object_id']]
        time.sleep(1)
        return options

    # Возвращает количество подписчиков
    def get_count_subs(self):
        subs_type = self.get_id()
        sub = 0
        try:
            if subs_type[0] == 'group':
                response_subs = requests.get("https://api.vk.com/method/groups.getMembers",
                                             params=
                                             {"group_id": subs_type[1],
                                              "access_token": self.__token,
                                              "v": self.__version
                                              }
                                             )
                time.sleep(1)
                return response_subs.json()['response']['count']
            if subs_type[0] == 'user':
                response_subs = requests.get("https://api.vk.com/method/users.getFollowers",
                                             params=
                                             {"user_id": subs_type[1],
                                              "access_token": self.__token,
                                              "v": self.__version
                                              }
                                             )
                time.sleep(1)
                if response_subs is not None:
                    sub = response_subs.json()['response']['count']

                response_friend = requests.get("https://api.vk.com/method/friends.get",
                                               params=
                                               {"user_id": subs_type[1],
                                                "fields": self.__domain,
                                                "access_token": self.__token,
                                                "v": self.__version
                                                }
                                               )
                time.sleep(1)
                friend = response_friend.json()['response']['count']
                subs = sub + friend
                return subs
        except:
            print("Ошибка чтения кол-ва подписчиков\n Укажите число ваших подписчиков:")
            subs = int(input())
            return subs

    # Возвращает массив, где выведенео количество упоминаний в посте
    def __check_count_id(self):
        count_id = []
        for text in self.__id_text:
            if text is not None:
                count_id.append(text[1].count("id"))
            else:
                count_id.append(0)
        return count_id

    # Получаем все посты с сервера
    def __get_posts(self):
        offset = 0
        count = 500
        count_post = 0
        while offset < 1000:
            response = requests.get("https://api.vk.com/method/wall.get",
                                    params=
                                    {
                                        "access_token": self.__token,
                                        "v": self.__version,
                                        "domain": self.__domain,
                                        "count": count,
                                        "offset": offset
                                    }
                                    )
            data = response.json()['response']['items']
            count_post = response.json()['response']['count']
            if len(data) == 0:
                break
            count_post += len(data)
            print('UPLOAD_POST=', count_post)
            offset += 100
            self.__all_posts.extend(data)
            time.sleep(2)

        self.__user_date_convert_to_unix(self.__enter_date)

        return self.__all_posts

    def __user_date_convert_to_unix(self,date):
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        self.__user_date = date.timestamp()

    # Получает данные о постах
    def __sort_post(self, x):
        for i in range(len(x)):
            if x[i]['date'] > self.__user_date:
                if x[i]['from_id'] * -1 == self.get_id()[1] and 'copy_history' not in x[i]:
                    item = [x[i]['likes']['count'], x[i]['views']['count'], x[i]['comments']['count'],
                            x[i]['reposts']['count'], x[i]['id'], x[i]['attachments'][0]['type'], x[i]['date'],
                            x[i]['text']]
                    self.__likes_views.append([item[0], item[1]])
                    self.__likes_comm_reposts.append([int(item[4]), int(item[0]), int(item[2]), int(item[3])])
                    self.__id_date.append([item[4], item[6]])
                    self.__id_text.append([item[4], item[7]])
                    self.__id_type.append([item[4], item[5], item[6]])

                if x[i]['attachments']:
                    print("SORTED - ", i, x[i]['attachments'][0]['type'], x[i]['id'])
                else:
                    print(x[i]['id']," - NOT SORTED")
        if len(x) == 0:
            return 'Постов по выбранной дате не найдено'
        print("end work sort_posts")
        self.rate = self.__engagement_rate()

    def __time_matrix(self):
        self.__best_choice = []
        sr_0810 = []
        sr_1012 = []
        sr_1214 = []
        sr_1416 = []
        sr_1618 = []
        sr_1820 = []
        sr_2008 = []
        rate = self.rate
        for i in range(len(self.__id_type)):
            time_post = int(datetime.datetime.fromtimestamp(self.__id_type[i][2]).strftime("%H"))

            if 8 <= time_post <= 10:
                sr_0810 += [['0810', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            if 10 < time_post <= 12:
                sr_1012 += [['1012', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            if 12 < time_post <= 14:
                sr_1214 += [['1214', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            if 14 < time_post <= 16:
                sr_1416 += [['1416', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            if 16 < time_post <= 18:
                sr_1618 += [['1618', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            if 18 < time_post <= 20:
                sr_1820 += [['1820', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]
            else:
                sr_2008 += [['2008', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0]]]

        self.__best_type(sr_0810)
        self.__best_type(sr_1012)
        self.__best_type(sr_1214)
        self.__best_type(sr_1416)
        self.__best_type(sr_1618)
        self.__best_type(sr_1820)
        self.__best_type(sr_2008)

    def __best_type(self, sr_time):
        photos = []
        videos = []
        photos_rate = 0
        videos_rate = 0
        if len(sr_time) != 0:
            for i in range(len(sr_time)):
                if sr_time[i][2] == 'photo' or sr_time[i][2] == 'album':
                    photos.append(sr_time[i][4])
                if sr_time[i][2] == 'video':
                    videos.append(sr_time[i][4])
            if len(photos) != 0:
                photos_rate = sum(photos) / int(len(photos))
            if len(videos) != 0:
                videos_rate = sum(videos) / int(len(videos))
            if photos_rate > videos_rate:
                self.__best_choice.append([sr_time[0][0], photos_rate, 'photos'])
            if photos_rate < videos_rate:
                self.__best_choice.append([sr_time[0][0], videos_rate, 'videos'])

            if sr_time[0][2] == 'photo':
                self.__photos_all.append(
                    [int(datetime.datetime.fromtimestamp(sr_time[0][3]).strftime("%H%M")), photos_rate])
            if sr_time[0][2] == 'video':
                self.__videos_all.append(
                    [int(datetime.datetime.fromtimestamp(sr_time[0][3]).strftime("%H%M")), videos_rate])

    def __optimal_time_post(self):
        self.__time_matrix()
        matrix = self.__best_choice
        index_max_stat_time_photo = 0
        index_max_stat_time_video = 0
        # create graph
        data_analys.graph_data_eng_type(self.__photos_all, self.__videos_all)
        matrix_time = []
        max_ph = 0
        max_vid = 0
        k = 0
        time_vid = ' '
        time_ph = ' '
        flag_videos = False
        flag_photos = False
        for i in matrix:
            if i[2] == 'photos':
                flag_photos = True
            if i[2] == 'videos':
                flag_videos = True
            if i[2] == 'photos' and i[1] > max_ph:
                max_ph = i[1]
                index_max_stat_time_photo = k
            if i[2] == 'videos' and i[1] > max_vid:
                max_vid = i[1]
                index_max_stat_time_video = k
            k += 1

        if flag_photos:
            time_ph = matrix[index_max_stat_time_photo][0][0:2] + ':00 - ' + matrix[index_max_stat_time_photo][0][
                                                                             2:4] + ':00' + ": " + \
                      matrix[index_max_stat_time_photo][2]
            time_photo_post = [self.get_id()[1],matrix[index_max_stat_time_photo][0], matrix[index_max_stat_time_photo][1],
                               matrix[index_max_stat_time_photo][2]]
            matrix_time.append(time_photo_post)
        else:
            matrix_time.append([])
        if flag_videos:
            time_vid = matrix[index_max_stat_time_video][0][0:2] + ':00 - ' + matrix[index_max_stat_time_video][0][
                                                                              2:4] + ':00' + ": " + \
                       matrix[index_max_stat_time_video][2]
            time_video_post = [self.get_id()[1],matrix[index_max_stat_time_video][0], matrix[index_max_stat_time_video][1],
                               matrix[index_max_stat_time_video][2]]
            matrix_time.append(time_video_post)
        else:
            matrix_time.append([])

        print(time_vid, time_ph)
        return matrix_time

    # Вычисление стандартного отклонения
    def __std(self, x):
        std_result = 0
        mean = sum(x) / len(x)
        for a in x:
            std_result += (a - mean) ** 2 / (len(x) - 1)
        return math.sqrt(std_result)

    # Возвращает массив с оценкой вовлечённости для каждого поста
    def __engagement_rate(self):
        x = self.__likes_comm_reposts
        rate = []
        subs = self.get_count_subs()
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(subs))])
        return rate

    # Вычисляет сумму массива по n элементу
    def __summ(self, x, n):
        summ_m = 0
        for i in x:
            summ_m += i[n]
        return summ_m

    # Вычисляет значение ковариации
    def __cov(self, x):
        cov_result = 0
        avg_x = self.__summ(x, 0) / len(x)
        avg_y = self.__summ(x, 1) / len(x)
        for i in range(len(x)):
            cov_result += (x[i][0] - avg_x) * (x[i][1] - avg_y)
        cov_result /= (len(x) - 1)
        return cov_result

    # Вычисляет значение коэфициента регрессионного анализа
    def __regr_analys(self, x):
        r = self.__cov(x) / (self.__std([xi[1] for xi in x]) * self.__std([yi[0] for yi in x]))
        return r

    def test(self):
        self.print_analyse()

    # Анализирует данные
    def analyse_data(self):

        self.__sort_post(self.__get_posts())

        last_post_time_likes_delta = []

        rate_engagement = self.rate

        count_id = self.__check_count_id()
        count_id_rate = []

        if sum(count_id_rate) > 0:
            for i in range(len(count_id)):
                count_id_rate.append([count_id[i], rate_engagement[i][0]])
        for i in range(len(self.__id_date) // 2 + 1):
            self.__delta_date_post = self.__id_date[i][1] - self.__id_date[i + 1][1]
            delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
            last_post_time_likes_delta.append([self.__delta_date_post, delta_rate_engagement_post])
        if sum(count_id_rate) > 0:
            regr_analys_id = self.__regr_analys(count_id_rate)
        else:
            regr_analys_id = 0
        reg_analys_views = self.__regr_analys(self.__likes_views)
        reg_analys_date_delta = self.__regr_analys(last_post_time_likes_delta)
        time_ph, time_vid = self.__optimal_time_post()
        return reg_analys_views, reg_analys_date_delta, regr_analys_id, time_ph, time_vid

    def print_analyse(self):
        reg_analys_views, reg_analys_date_delta, regr_analys_id, time_ph, time_vid = self.analyse_data()
        print("Зависимость вовлечённости от просмотров - ", round(reg_analys_views, 2))
        print("Зависимость вовлеченности от времени публикации между постами - ", reg_analys_date_delta)
        print("Зависимость вовлеченности от использованных отметок ", regr_analys_id)
        if len(time_ph) != 0:
            print("Лучшее время для поста фотографий:", str(time_ph[1])[0:2] + ':00 - ' + str(time_ph[1])[2:4] + ':00')
        else:
            print("Фотографий за выбранный период не найдено, советую разнообразить свой контент и добавить их!")
        if len(time_vid) != 0:
            print("Лучшее время для поста видео:"    , str(time_vid[1])[0:2] + ':00 - ' +str(time_vid[1])[2:4] + ':00')
        else:
            print("Видеороликов за выбранный период не найдено, советую разнообразить свой контент и добавить их!")

