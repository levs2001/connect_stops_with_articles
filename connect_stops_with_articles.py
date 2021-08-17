import datetime
import csv

STOPBEGTIME_IND = 4
STOPENDTIME_IND = 5

PRODBEGTIME_IND = 3
PRODENDTIME_IND = 4

ARTICLE_PROD_IND = 0

ARTICLE_GRAMM_IND = 1
GRAMM_IND = 3

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

GRAMM_FILENAME = "gramm_code_prod.csv"


def get_date_obj(str_date):
    try:
        time_obj = datetime.datetime.strptime(str_date, DATE_FORMAT)
        # print(begtime_obj)
        return time_obj
    except ValueError:
        print("Not date was ignored: " + str_date)
        return str_date


def write_gramm_dict(gramm_filename):
    with open(GRAMM_FILENAME, encoding="utf-8") as gramm_f:
        gramm_r = csv.reader(gramm_f)
        gramm_dict = {}
        for row in gramm_r:
            gramm_dict.update({row[ARTICLE_GRAMM_IND]: row[GRAMM_IND]})
        gramm_dict.pop("Product Asigned")
        return gramm_dict


if __name__ == '__main__':
    STOPS_FILENAME = input("Enter stops filename: ")
    ARTS_FILENAME = input("Enter articles filename: ")
    STOPS_ARTS_FILENAME = input("Enter new stops with articles filename: ")

    stops = []
    articles = []

    # Записываем таблицы в список, меняя строковые даты на объекты datetime
    with open(STOPS_FILENAME, encoding="utf-8") as stops_f:
        stops_r = csv.reader(stops_f)
        for row in stops_r:
            row[STOPBEGTIME_IND] = get_date_obj(row[STOPBEGTIME_IND])
            row[STOPENDTIME_IND] = get_date_obj(row[STOPENDTIME_IND])
            stops.append(row)

    with open(ARTS_FILENAME, encoding="utf-8") as articles_f:
        articles_r = csv.reader(articles_f)
        for row in articles_r:
            row[PRODBEGTIME_IND] = get_date_obj(row[PRODBEGTIME_IND])
            row[PRODENDTIME_IND] = get_date_obj(row[PRODENDTIME_IND])
            articles.append(row)
    ####

    # Удаляем строки заголовков
    stops_title = stops.pop(0)
    articles.pop(0)
    ####

    try:
        gramm_dict = write_gramm_dict(GRAMM_FILENAME)
    except FileNotFoundError:
        print("Grammage file not found! Writing will be without it.")

    # Вставляем в таблицу стопов артикул, на котором произошла остановка
    for stop in stops:
        for article in articles:
            if (stop[STOPBEGTIME_IND] >= article[PRODBEGTIME_IND] and stop[STOPBEGTIME_IND] <= article[
                PRODENDTIME_IND]):
                stop.append(article[ARTICLE_PROD_IND])
                if article[ARTICLE_PROD_IND] in gramm_dict:
                    stop.append(gramm_dict[article[ARTICLE_PROD_IND]])
                else:
                    stop.append("-1")
                break
    ####

    # Записываем всю информацию в новый csv файл
    with open(STOPS_ARTS_FILENAME, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        for stop in stops:
            stop[STOPBEGTIME_IND] = stop[STOPBEGTIME_IND].strftime(DATE_FORMAT)
            stop[STOPENDTIME_IND] = stop[STOPENDTIME_IND].strftime(DATE_FORMAT)
        stops_title.append("ARTNO")
        stops_title.append("GRAMMAGE")
        stops.insert(0, stops_title)
        writer.writerows(stops)
    ####
