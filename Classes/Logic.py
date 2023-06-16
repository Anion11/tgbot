import datetime
# import DataGraph
from settings import *
from Classes.Utils import *

class Logic:
    def __init__(self, domain, date):
        self.__id_type = []
        self.__delta_date_post = []
        self.__id_text = []
        self.__id_date = []
        self.__likes_comm_reposts = []
        self.__likes_views = []
        self.__best_choice = []
        self.__domain = domain
        self.__all_posts = []
        self.__photos_all = []
        self.__videos_all = []
        self.__enter_date = date

    # Получение id пользователя
    def get_id(self):
        response_subs = vk_session.method("utils.resolveScreenName",{ "screen_name": self.__domain})
        options = [response_subs['type'], response_subs['object_id']]
        return options

    # Возвращает количество подписчиков
    def get_count_subs(self):
        subs_type = self.get_id()
        sub = 0
        try:
            if subs_type[0] == 'group':
                response_subs = vk_session.method("groups.getMembers",{"group_id": subs_type[1]})
                return response_subs['count']
            if subs_type[0] == 'user':
                response_subs = vk_session.method("users.getFollowers",{"user_id": subs_type[1]})
                if response_subs is not None:
                    sub = response_subs['count']

                response_friend = vk_session.method("friends.get",{"user_id": subs_type[1],"fields": self.__domain})
                friend = response_friend['count']
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
            response = vk_session.method("wall.get",{"domain": self.__domain,"count": count, "offset": offset})
            data = response['items']
            if len(data) == 0:
                break
            count_post += len(data)
            print('UPLOAD_POST=', count_post)
            offset += 100
            self.__all_posts.extend(data)
        
        self.__user_date = Utils.user_date_convert_to_unix(self.__enter_date)
        return self.__all_posts

    # Получает данные о постах
    def __sort_post(self, x):
        for i in range(len(x)):
            try:
                if x[i]['date'] > self.__user_date:
                    if x[i]['from_id'] == self.get_id()[1] and 'copy_history' not in x[i]:
                        item = [x[i]['likes']['count'], x[i]['views']['count'], x[i]['comments']['count'],
                                x[i]['reposts']['count'], x[i]['id'], x[i]['attachments'][0]['type'], x[i]['date'],
                                x[i]['text']]
                        print(item)
                        self.__likes_views.append([item[0], item[1]])
                        self.__likes_comm_reposts.append([int(item[4]), int(item[0]), int(item[2]), int(item[3])])
                        self.__id_date.append([item[4], item[6]])
                        self.__id_text.append([item[4], item[7]])
                        self.__id_type.append([item[4], item[5], item[6]])

                    if x[i]['attachments']:
                        print("SORTED - ", i, x[i]['attachments'][0]['type'], x[i]['id'])
                    else:
                        print(x[i]['id']," - NOT SORTED")
            except:
                break
        if len(self.__id_date) <= 1:
            return -1
        print("end work sort_posts")
        self.rate = self.__engagement_rate()

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
                    

            time_matrix()
            matrix = self.__best_choice
            index_max_stat_time_photo = 0
            index_max_stat_time_video = 0
            # create graph
            # data_analys.graph_data_eng_type(self.__photos_all, self.__videos_all)
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
    # Возвращает массив с оценкой вовлечённости для каждого поста
    def __engagement_rate(self):
        x = self.__likes_comm_reposts
        rate = []
        subs = self.get_count_subs()
        for j in x:
            rate.append([((j[1] + j[2] + j[3]) / int(subs))])
        return rate
    def test(self):
        self.print_analyse()

    # Анализирует данные
    def analyse_data(self):

        x = self.__sort_post(self.__get_posts())
        if(x == -1):
            return  -1
        last_post_time_likes_delta = []

        rate_engagement = self.rate

        count_id = self.__check_count_id()
        count_id_rate = []

        if sum(count_id_rate) > 0:
            for i in range(len(count_id)):
                count_id_rate.append([count_id[i], rate_engagement[i][0]])
        for i in range(len(self.__id_date) // 2 - 1):
                self.__delta_date_post = self.__id_date[i][1] - self.__id_date[i + 1][1]
                delta_rate_engagement_post = rate_engagement[i][0] - rate_engagement[i + 1][0]
                last_post_time_likes_delta.append([self.__delta_date_post, delta_rate_engagement_post])
        reg_analys_date_delta = Utils.regr_analys(last_post_time_likes_delta)
        if sum(count_id_rate) > 0:
            regr_analys_id = Utils.regr_analys(count_id_rate)
        else:
            regr_analys_id = 0
        reg_analys_views = Utils.regr_analys(self.__likes_views)

        time_ph, time_vid = self.__optimal_time_post()
        return reg_analys_views, reg_analys_date_delta, regr_analys_id, time_ph, time_vid

    def print_analyse(self):
        if(self.analyse_data() != -1):
            reg_analys_views, reg_analys_date_delta, regr_analys_id, time_ph, time_vid = self.analyse_data()
        else:
            return
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

