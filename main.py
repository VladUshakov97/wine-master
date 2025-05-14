from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from collections import defaultdict
import pandas
from dotenv import load_dotenv
import os


def get_year_word(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    last_number = age % 10
    if last_number == 1:
        return "год"
    elif 2 <= last_number <= 4:
        return "года"
    else:
        return "лет"

def main():
    load_dotenv()
    file_path = os.getenv('WINE_FILE_PATH', 'assortment.xlsx')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
        )
    template = env.get_template('template.html')
    wines = pandas.read_excel(file_path, keep_default_na=False)
    all_wines = wines.to_dict(orient='records')

    grouped_categories = defaultdict(list)

    for wine in all_wines:
        category = wine['Категория']
        drink_info = {
            'Название': wine['Название'],
            'Сорт': wine['Сорт'],
            'Цена': wine['Цена'],
            'Картинка': wine['Картинка'],
            'Акция': wine['Акция']
        }
        grouped_categories[category].append(drink_info)

    year_of_creation = 1920
    now_year = datetime.now().year
    age = now_year - year_of_creation
    year = declension_of_year(age)

    rendered_page = template.render(
        age=age,
        year=year,
        wines=grouped_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
if __name__ == "__main__":
    main()
