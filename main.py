from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from collections import defaultdict
import pandas

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')


def year_word(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    last_number = age % 10
    if last_number == 1:
        return "год"
    elif 2 <= last_number <= 4:
        return "года"
    else:
        return "лет"


wines = pandas.read_excel('assortment.xlsx', keep_default_na=False)
all_wines = wines.to_dict(orient='records')

grouped = defaultdict(list)

for wine in all_wines:
    category = wine['Категория']
    drink_info = {
        'Название': wine['Название'],
        'Сорт': wine['Сорт'],
        'Цена': wine['Цена'],
        'Картинка': wine['Картинка'],
        'Акция': wine['Акция']
    }
    grouped[category].append(drink_info)

then_year = 1920
now_year = datetime.now().year
age = now_year - then_year
year = year_word(age)

rendered_page = template.render(
    age=age,
    year=year,
    wines=dict(grouped)
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
