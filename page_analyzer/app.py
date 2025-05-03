import os

import psycopg2
import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from psycopg2.extras import DictCursor

from page_analyzer.dao import UrlDAO
from page_analyzer.utils import parse_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
dao = UrlDAO(conn)


@app.route("/", methods=['GET', 'POST'])
def index():
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'POST':
        url = request.form.get('url')

        based_url = parse_url(url)

        if not validators.url(url):
            flash("Некорректный URL", "danger")
            return redirect(url_for('index'))

        id_returned, is_existed = dao.save(based_url)
        if is_existed:
            flash("Страница уже существует", "info")
        else:
            flash("Страница успешно добавлена", "success")
        return redirect(url_for('get_url', id=id_returned))

    return render_template('index.html', messages=messages)


@app.get("/urls/<int:id>")
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    row = dao.get_by_id(id)
    url_checks = dao.get_checks_by_url_id(id)
    if not row:
        return render_template("not_found.html")
    return render_template("view.html", messages=messages, row=row, url_checks=url_checks)


@app.get("/urls")
def get_url_list():
    list = dao.get_all()
    return render_template("list.html", list=list)


@app.post("/urls/<int:id>/checks")
def add_check_url(id):
    row = dao.get_by_id(id)
    try:
        res = requests.get(row["name"])
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        meta_description = soup.find("meta", attrs={"name": "description"})
        meta_description_content = meta_description.get("content") if meta_description else ""

        h1_tag = soup.find("h1")
        h1_text = h1_tag.text if h1_tag else ""

        title_tag = soup.title
        title_text = title_tag.text if title_tag else ""

        dao.create_url_check(id, res.status_code, h1_text, title_text, meta_description_content)
    except requests.exceptions.HTTPError:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for('get_url', id=id))
