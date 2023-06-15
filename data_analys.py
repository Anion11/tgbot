import matplotlib.pyplot as plt
def graph_data_eng_type(photo, video):
    # Создание нового холста и размещение двух графиков на нем
    photo = sorted(photo, key=lambda x: x[0])
    video = sorted(video, key=lambda x: x[0])
    DATE_POST_PHOTO = []
    ENG_RATE_PHOTO  = []
    DATE_POST_VIDEO = []
    ENG_RATE_VIDEO  = []
    DATE_POST_PHOTO += [xi[0] for xi in photo]
    ENG_RATE_PHOTO  += [xi[1] for xi in photo]
    DATE_POST_VIDEO += [xi[0] for xi in video]
    ENG_RATE_VIDEO  += [xi[1] for xi in video]
    fig, axes = plt.subplots(nrows=2, ncols=1)


    # Построение первого графика
    axes[0].plot(DATE_POST_PHOTO, ENG_RATE_PHOTO, 'r--')
    axes[0].set_title('Дата фото поста - Вовлечённость')

    # Построение второго графика
    axes[1].plot(DATE_POST_VIDEO, ENG_RATE_VIDEO, 'r--')
    axes[1].set_title('Дата видео поста - Вовлечённость')

    # Отображение графиков
    plt.tight_layout()
    plt.show()

