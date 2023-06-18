import datetime
# import DataGraph
from settings import *
from Classes.Utils import *

class Statistic:
    def __init__(self, domain, date):
        self.sovet = None
        self.__enter_date = date
        self.__domain = domain
        self.__id_date = []
        self.__likes_comm_reposts = []
        self.__id_text = []
        self.__delta_date_post = []
        self.__id_type = []
        self.__likes_views = []
        self.__best_choice = []
        self.__photos_all = []
        self.__videos_all = []
        self.__all_posts = []
        self.__flag_program = False
        self.__sort_post(self.__get_posts())
        self.__average_engagement = self.__average_engagement_rate()


        # Получение id пользователя
    def get_id(self):
        response_subs = vk_session.method("utils.resolveScreenName",{ "screen_name": self.__domain})
        options = [response_subs['type'], response_subs['object_id']]
        if(response_subs['type'] == 'group'):
            options[1] *= -1
        return options
    # Возвращает количество подписчиков
    def get_count_subs(self):
        subs_type = self.get_id()
        if subs_type[0] == 'group':
            response_subs = vk_session.method("groups.getMembers",{"group_id": -1 * subs_type[1]})
            return Utils.get_count_subs_group(subs_type, response_subs)
        if subs_type[0] == 'user':
            response_subs = vk_session.method("users.getFollowers",{"user_id": subs_type[1]})
            response_friend = vk_session.method("friends.get",{"user_id": subs_type[1],"fields": self.__domain})
            return Utils.get_count_subs_user(subs_type, response_subs, response_friend)

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
        self.__user_date_convert_to_unix(self.__enter_date)
        offset = 0
        count = 500
        count_post = 0
        while offset < 500:
            response = vk_session.method("wall.get",{"domain": self.__domain,"count": count, "offset": offset})
            data = response['items']
            if len(data) == 0:
                break
            count_post += len(data)
            offset += 100
            self.__all_posts.extend(data)
        
        self.__user_date = Utils.user_date_convert_to_unix(self.__enter_date)
        return self.__all_posts

    # Конвертирует unix в datetime
    def __user_date_convert_to_unix(self, date):
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        self.__user_date = date.timestamp()

    # Получает данные о постах
    def __sort_post(self, x):
        k = 0
        id_user = self.get_id()[1]
        for i in range(len(x)):
            if x[i]['date'] >= self.__user_date and (
                    abs(x[i]['from_id']) == id_user and 'copy_history' not in x[i]):
                try:
                    item = [x[i]['likes']['count'], x[i]['views']['count'], x[i]['comments']['count'],
                            x[i]['reposts']['count'], x[i]['id'], x[i]['attachments'][0]['type'], x[i]['date'],
                            x[i]['text']]
                    self.__likes_views.append([item[0], item[1]])
                    self.__likes_comm_reposts.append([int(item[4]), int(item[0]), int(item[2]), int(item[3])])
                    self.__id_date.append([item[4], item[6]])
                    self.__id_text.append([item[4], item[7]])
                    self.__id_type.append([item[4], item[5], item[6]])
                    k += 1
                    print("SORTED - ", i, x[i]['attachments'][0]['type'], x[i]['id'])
                    if x[i]['attachments']:
                        pass
                    else:
                        print(x[i]['id'], " - REPOST NOT SORTED")
                except:
                    pass
        if len(self.__id_type) <= 1:
            self.__flag_program = True
            return


    def __optimal_time_post(self):
        def time_matrix():
            self.__best_choice = []
            sr_0810 = []
            sr_1012 = []
            sr_1214 = []
            sr_1416 = []
            sr_1618 = []
            sr_1820 = []
            sr_2008 = []
            rate = self.__engagement_rate()
            print(self.__id_type)
            for i in range(len(self.__id_type)):
                time_post = datetime.datetime.fromtimestamp(self.__id_type[i][2]).time()

                if datetime.time(8, 0) <= time_post <= datetime.time(10, 0):
                    sr_0810 += [['0810', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(10, 0) < time_post <= datetime.time(12, 0):
                    sr_1012 += [['1012', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(12, 0) < time_post <= datetime.time(14, 0):
                    sr_1214 += [['1214', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(14, 0) < time_post <= datetime.time(16, 0):
                    sr_1416 += [['1416', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(16, 0) < time_post <= datetime.time(18, 0):
                    sr_1618 += [['1618', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(18, 0) < time_post <= datetime.time(20, 0):
                    sr_1820 += [['1820', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]
                if datetime.time(20, 0) < time_post <= datetime.time(23, 59) or \
                   datetime.time(00,00) < time_post <= datetime.time(8, 00):
                    sr_2008 += [['2008', self.__id_type[i][0], self.__id_type[i][1], self.__id_type[i][2], rate[i][0],
                                 self.__likes_views[i][1]]]

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

        time_matrix()
        matrix = self.__best_choice
        index_max_stat_time_photo = 0
        index_max_stat_time_video = 0
        matrix_time = []
        max_ph = 0
        max_vid = 0
        k = 0
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
            time_photo_post = [self.get_id()[1], matrix[index_max_stat_time_photo][0],
                               matrix[index_max_stat_time_photo][1],
                               matrix[index_max_stat_time_photo][2]]
            matrix_time.append(time_photo_post)
        else:
            matrix_time.append([])
        if flag_videos:
            time_video_post = [self.get_id()[1], matrix[index_max_stat_time_video][0],
                               matrix[index_max_stat_time_video][1],
                               matrix[index_max_stat_time_video][2]]
            matrix_time.append(time_video_post)
        else:
            matrix_time.append([])
        return matrix_time

    # Возвращает массив с оценкой вовлечённости для каждого поста
    def __engagement_rate(self):
        x = self.__likes_comm_reposts
        rate = []
        subs = self.get_count_subs()
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(subs)), j[0]])
        return rate

    def __average_engagement_rate(self):
        all_engagement = [x[0] for x in self.__engagement_rate()]
        return sum(all_engagement)/len(all_engagement)

    def check_engagement_rate_post(self, id):
        er = self.__engagement_rate()
        for post in er:
            if post[1] == id:
                self.equal_engagement_rate(post[0])
                return post[0]

    # Анализирует данные
    def equal_engagement_rate(self, eng_coef):
        if eng_coef > self.__average_engagement:
            self.sovet = ("Коэффициент engagement rate выше среднего значения на странице. Это хороший результат! \n "
                          "Пользователям понравился ваш контент. Продолжайте в том же духе!")
        elif eng_coef < self.__average_engagement:
            self.sovet = ("Коэффициент engagement rate ниже среднего значения на странице.\n"
                       "Значит, пользователи не очень заинтересовались вашим контентом.\n"
                       "Советуем попробовать что-то новое! Может быть, изменить формат или тему поста?")
        else:
            self.sovet = ("Коэффициент engagement rate равен среднему значению на странице.\n"
                          "Такой результат может быть как хорошим, так и плохим.\n"
                          "Постарайтесь прислушаться к комментариям и отзывам пользователей, чтобы улучшить свой контент в будущем.")
    def analyse_data(self):
        utils = Utils()
        if self.__flag_program:
            return
        rate_engagement = self.__engagement_rate()
        count_id = self.__check_count_id()
        last_post_time_likes_delta = []
        count_id_rate = []
        delta_time_post = 0
        if sum(count_id_rate) > 0:
            for i in range(len(count_id)):
                count_id_rate.append([count_id[i], rate_engagement[i][0]])
        for i in range(len(self.__id_date) // 2 + 1):
            self.__delta_date_post = self.__id_date[i][1] - self.__id_date[i + 1][1]
            delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
            last_post_time_likes_delta.append([self.__delta_date_post, delta_rate_engagement_post])
            delta_time_post += self.__delta_date_post
        if sum(count_id_rate) > 0:
            regr_analys_id = Utils.regr_analys(count_id_rate)
        else:
            regr_analys_id = 0
        reg_analys_views = Utils.regr_analys(self.__likes_views)
        reg_analys_date_delta = Utils.regr_analys(last_post_time_likes_delta)
        sr_delta_time_post = delta_time_post // len(last_post_time_likes_delta)
        self.time_ph, self.time_vid = self.__optimal_time_post()
        return reg_analys_views, reg_analys_date_delta, regr_analys_id, self.time_ph, self.time_vid, sr_delta_time_post


    def print_analyse(self):
        if self.__flag_program:
            return
        reg_analys_views, reg_analys_date_delta, regr_analys_id, time_ph, time_vid, sr_delta_time_post = self.analyse_data()

        self.strVovlViews = "Зависимость вовлечённости от просмотров - " + str(round(reg_analys_views, 2))
        self.strVovlDate = "Зависимость вовлеченности от времени публикации между постами - " + str(reg_analys_date_delta)
        self.strVovlOtm = "Зависимость вовлеченности от использованных отметок " + str(regr_analys_id)
        if len(time_ph) != 0:
            self.timeToPhoto = "Лучшее время для поста фотографий:" + str(time_ph[1])[0:2] + ':00 - ' + str(time_ph[1])[2:4] + ':00'
        else:
            self.timeToPhoto = "Фотографий за выбранный период не найдено, советую разнообразить свой контент и добавить их!"
        if len(time_vid) != 0:
            self.timeToVideo = "Лучшее время для поста видео:"  + str(time_vid[1])[0:2] + ':00 - ' + str(time_vid[1])[2:4] + ':00'
        else:
            self.timeToVideo = "Видеороликов за выбранный период не найдено, советую разнообразить свой контент и добавить их!"