from bs4 import BeautifulSoup
import requests
import collections
from stemmer import *
from lsi_words_parser.db import db
from lsi_words_parser.models import LSI
from lsi_words_parser import cel

XML_KEY = ''


class Parser:

    def __init__(self, request='', url=''):
        self.request = request
        self.url = url if url else self.make_url_for_parcing()
        self.page_html = self.get_html()

    def make_url_for_parcing(self):
        return f'http://xmlriver.com/search_yandex/xml?user=1391&key={XML_KEY}&query={self.request}'

    def get_html(self):
        if not self.is_pdf():
            try:
                response = requests.get(self.url, verify=False, timeout=15).content
            except:
                print('Доступ к сайту не получен')
                response = ''
            return BeautifulSoup(response, 'html.parser')

    def get_all_sites_urls(self):
        all_sites_data = self.get_all_sites_data()
        return [site_data.find('url').text for site_data in all_sites_data]

    def get_all_sites_data(self):
        return self.page_html.find_all('doc')

    def is_pdf(self):
        if '.pdf' in self.url[-4:]:
            return True


class Content:

    def __init__(self, html):
        self.html = html
        self.all_words_on_page = self.get_all_words()
        self.unique_words = self.get_unique_words()

    def get_all_words(self):
        text_with_newlines = self.html.get_text()
        text_without_newlines = text_with_newlines.replace('\n\n', '')
        text_without_newlines = text_without_newlines.replace('\n', ' ')
        return text_without_newlines.split()

    def get_unique_words(self):
        unique_words = set(self.all_words_on_page)
        unique_words = stem_text(unique_words, is_punctuation_needed=False)
        return set(unique_words)


class LsiStatistic:
    def __init__(self, sites_contents):
        self.valid_sites = 0
        self.sites_contents = sites_contents
        self.counted_words = self.count_words_in_site_content()

    def count_words_in_site_content(self):
        words_counter = collections.Counter()
        for site_content in self.sites_contents:
            if len(site_content.unique_words) > 100:
                self.valid_sites += 1
                for word in site_content.unique_words:
                    words_counter[word] += 1

        return words_counter

    def count_word_percent_in_site_content(self):
        word_percent = dict()
        del self.counted_words['']

        for word, count in self.counted_words.items():
            word_percent[word] = int(count / self.valid_sites * 100)

        word_percent = {k: v for k, v in sorted(word_percent.items(), key=lambda item: item[1], reverse=True)}

        return word_percent


class LsiStatisticDB:

    @classmethod
    def add_lsi_statistic_to_db(cls, lsi_statistic, request_id):
        new_requests = [LSI(text=word, percent=percent, request_id=request_id) for word, percent in lsi_statistic.items()
                        if percent >= 50]
        db.bulk_save_objects(new_requests)
        db.commit()


class Manager:

    def __init__(self, user_requests):
        self.requests = user_requests
        self.start()

    def start(self):
        for request in self.requests:
            sites_content = self.get_sites_contents(request['text'])
            lsi_statistic = self.get_lsi_statistic(sites_content)
            LsiStatisticDB.add_lsi_statistic_to_db(lsi_statistic, request['id'])

    @staticmethod
    def get_sites_contents(request):
        parser = Parser(request=request)
        sites_urls = parser.get_all_sites_urls()
        parsed_sites = [Parser(url=site_url) for site_url in sites_urls]
        return [Content(site.page_html) for site in parsed_sites]

    @staticmethod
    def get_lsi_statistic(sites_content):
        lsi_statistic = LsiStatistic(sites_content)
        lsi_statistic = lsi_statistic.count_word_percent_in_site_content()
        return lsi_statistic


@cel.task
def run(user_requests):
    Manager(user_requests)