from flask import render_template, redirect, request
from lsi_words_parser.form import NewRequestForm
from lsi_words_parser import app
from lsi_words_parser.logic.new_requests_handler import NewRequestHandler
from lsi_words_parser.logic.order_view import ViewHandler
from service.main import run


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def new_request():
    """
    Метод проверяет форму, и если она валидна:
    - подготавливает список запросов пользователя
    - проверяет доступны ли пользователю бесплатные запросы
    - если да, добавляет их в БД и создает задачу для Celery
    """
    form = NewRequestForm()
    if form.validate_on_submit():
        handler = NewRequestHandler()
        requests = handler.make_requests_list(form.requests.data)
        if handler.check_user_limit(request.remote_addr, len(requests)) <= 10 and len(requests) <= 10:
            added_requests = handler.add_new_data_to_database(requests)
            run.delay(added_requests)

            return redirect('/' + handler.short_link)
    return render_template('new_request.html', title='Новые запросы', form=form)


@app.route('/<short_link>')
def get_order_page(short_link):
    handler = ViewHandler(short_link)
    orders_data = handler.get_order_data()
    return render_template('order_page.html', title='Новые зfgdflgkdf', results=orders_data)



