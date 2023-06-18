import datetime
import math

class Utils:
    # Вычисление стандартного отклонения
    def std(self,x):
        std_result = 0
        mean = sum(x) / len(x)
        for a in x:
            std_result += (a - mean) ** 2 / (len(x) - 1)
        return math.sqrt(std_result)

    # Вычисляет сумму массива по n элементу
    def summ(self, x, n):
        summ_m = 0
        for i in x:
            summ_m += i[n]
        return summ_m

    # Вычисляет значение корреляции
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
    
    def user_date_convert_to_unix(date):
        date = date.replace(".", "/")
        date = date.replace("-", "/")
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        return date.timestamp()
    def get_count_subs_group(subs_type, response_subs):
        return response_subs['count']

    def get_count_subs_user(subs_type, response_subs, response_friend):
        sub = 0
        if response_subs is not None:
            sub = response_subs['count']
        friend = response_friend['count']
        subs = sub + friend
        return subs