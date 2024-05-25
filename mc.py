from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import pandas as pd


# Глобальная переменная для пути к файлу
FILE_PATH = 'data.csv'
def add_to_csv(rate):
    date=datetime.today().strftime('%Y-%m-%d')
    df = pd.read_csv(FILE_PATH, sep=';', parse_dates=['Дата'], dayfirst=True)
    if date in df['Дата'].values:
        # Обновление записи
        if (rate==1):
            df.loc[df['Дата'] == date, 'Позитивы'] +=1
        else:
            df.loc[df['Дата'] == date, 'Негативы'] +=1
    else:
        # Добавление новой записи
        if (rate==1):
            new_record = pd.DataFrame({'Дата': [date], 'Позитивы': [1], 'Негативы': [0]})
        else:
            new_record = pd.DataFrame({'Дата': [date], 'Позитивы': [0], 'Негативы': [1]})

        df = pd.concat([df, new_record], ignore_index=True)




def add_or_update_record(date, positives, negatives):
    # Загрузка данных из файла
    try:
        df = pd.read_csv(FILE_PATH, sep=';', parse_dates=['Дата'], dayfirst=True)
    except FileNotFoundError:
        # Если файл не существует, создаем пустой DataFrame с нужными столбцами
        df = pd.DataFrame(columns=['Дата', 'Позитивы', 'Негативы'])
        df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')

    date = pd.to_datetime(date, format='%d.%m.%Y')

    # Проверка наличия записи с данной датой
    if date in df['Дата'].values:
        # Обновление записи
        df.loc[df['Дата'] == date, 'Позитивы'] = positives
        df.loc[df['Дата'] == date, 'Негативы'] = negatives
    else:
        # Добавление новой записи
        new_record = pd.DataFrame({'Дата': [date], 'Позитивы': [positives], 'Негативы': [negatives]})
        df = pd.concat([df, new_record], ignore_index=True)

    # Сортировка по дате
    df = df.sort_values(by='Дата')

    # Сохранение данных обратно в файл
    df.to_csv(FILE_PATH, sep=';', index=False, date_format='%d.%m.%Y')

# Функция для фильтрации данных по датам и построения графика
def plot_data_with_date_range(df, start_date, end_date):
    # Фильтрация данных по заданному промежутку дат
    mask = (df['Дата'] >= start_date) & (df['Дата'] <= end_date)
    filtered_df = df.loc[mask]

    # Создание графика
    plt.figure(figsize=(10, 6))  # Увеличение размера графика

    # Закрашивание области для позитивов
    plt.fill_between(filtered_df['Дата'], filtered_df['Позитивы'], color='skyblue', alpha=0.4, label='Позитивы')

    # Закрашивание области для негативов
    plt.fill_between(filtered_df['Дата'], filtered_df['Негативы'], color='lightcoral', alpha=0.4, label='Негативы')

    # Линия для позитивов
    plt.plot(filtered_df['Дата'], filtered_df['Позитивы'], linestyle='-', color='blue')

    # Линия для негативов
    plt.plot(filtered_df['Дата'], filtered_df['Негативы'], linestyle='-', color='red')

    # Добавление заголовков и меток осей
    plt.title('Позитивы и Негативы по датам')
    plt.xlabel('Дата')
    plt.ylabel('Количество')

    # Поворот меток на оси X для лучшей читаемости
    plt.xticks(rotation=45)

    # Установка меток на оси X только для крайних дат выбранного промежутка
    plt.xticks([filtered_df['Дата'].min(), filtered_df['Дата'].max()],
               [filtered_df['Дата'].min().strftime('%d.%m.%Y'), filtered_df['Дата'].max().strftime('%d.%m.%Y')])

    # Добавление легенды
    plt.legend()

    # Отображение графика
    plt.tight_layout()  # Автоматическая подгонка размеров
    plt.savefig("image.png")


# Загрузка данных из файла
df = pd.read_csv('data.csv', sep=';')

# Преобразование столбца 'Дата' в тип данных datetime
df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')

# Пример использования функции
start_date = '2022-12-05'
end_date = '2022-12-07'

def predict_with_date_range(text:str):
    vectorizer = load("vector.joblib")  # или TfidfVectorizer(), если использовали его
    X_text = vectorizer.transform(pd.Series(str.lower(text)))
    model = load('model.joblib')
    ans=(model.predict(X_text))[0]
    wordlevel = load('wordlevel.joblib')
    ans+=(wordlevel.predict(X_text))[0]
    count_vectors = load('count_vectors.joblib')
    ans+=(count_vectors.predict(X_text))[0]
    log = load('log.joblib')
    ans+=(log.predict(X_text))[0]
    if ans<2:
        return 0
    else: return 1
#пример работы предикта
print(predict_with_date_range(" hate my friend, but I love him more than I hate him, so it's more like I love him than I hate him."))

