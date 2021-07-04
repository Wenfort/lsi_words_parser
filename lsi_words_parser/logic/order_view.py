from db import *
from lsi_words_parser.models import Order, Request, LSI


class ViewHandler:

    def __init__(self, short_link):
        self.short_link = short_link

    def get_requests_data_from_order(self):
        return db.query(Request.id, Request.text).join(Order, Request.order_id == Order.id). \
            where(Order.shortlink == self.short_link).all()

    def get_order_data(self):
        requests_data = self.get_requests_data_from_order()
        order_data = [self.get_lsi_data_from_request(request_data) for request_data in requests_data]

        return order_data

    def get_lsi_data_from_request(self, request_data):
        request_id, request_text = request_data[0], request_data[1]
        lsi_data = {'request_text': request_text, 'lsi_words': {}}
        requests_data = db.query(LSI.text, LSI.percent).where(LSI.request_id == request_id).all()
        for data in requests_data:
            lsi_text, lsi_percent = data[0], data[1]
            lsi_data['lsi_words'][lsi_text] = lsi_percent

        lsi_data['table_column_length'] = len(lsi_data['lsi_words']) / 3
        return lsi_data
