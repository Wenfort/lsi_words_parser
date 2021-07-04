from db import *
from lsi_words_parser.models import IpHistory, Request, Order
import hashlib

class NewRequestHandler:

    @staticmethod
    def make_requests_list(request):
        return request.replace('\r', '').split('\n')

    def check_user_limit(self, user_ip):
        request = db.query(IpHistory).where(IpHistory.ip == user_ip)
        row = db.execute(request).scalar()
        if row:
            row.counter += 1
        else:
            row = IpHistory(ip=user_ip, counter=1)
            db.add(row)
        db.commit()
        return row.counter

    def add_new_data_to_database(self, requests):
        order_id = self.add_new_order_and_return_id(requests)
        added_requests = self.add_new_requests_to_postgres(requests, order_id)
        return added_requests

    def make_short_link(self, requests):
        secret_word = 'lsi_words_hash'
        requests = ''.join(requests)

        short_link = hashlib.new('sha512_256')
        short_link.update(bytes(secret_word + requests, encoding='utf-8'))
        short_link = short_link.hexdigest()
        self.short_link = short_link

    def add_new_order_and_return_id(self, requests):
        self.make_short_link(requests)
        order = Order(shortlink=self.short_link)
        db.add(order)
        db.commit()
        return order.id

    def add_new_requests_to_postgres(self, requests, order_id):
        new_requests = [Request(text=request, order_id=order_id) for request in requests]
        db.bulk_save_objects(new_requests, return_defaults=True)
        db.commit()
        return [{'text': new_request.text, 'id': new_request.id} for new_request in new_requests]
