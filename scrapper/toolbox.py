from requests_html import HTMLSession
from fake_useragent import UserAgent
from random import uniform
from annonces.models import Annonce
from datetime import datetime
import time
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


class GetUrls():
    def __init__(self, search_url):
        self.search_url = search_url
        self.session = HTMLSession()
        self.ua = UserAgent()
        self.add_list = []
        self.get_urls()
        self._save_urls()

    def get_urls(self):
        while self.search_url:
            self._get()
            # grab urls
            for add_url in list(
                    filter(lambda x: "https://www.pap.fr/annonces" in x, self.response.html.absolute_links)):
                self.add_list.append(add_url)
            # grab next page
            if self.response.html.find("a#pagination-next"):
                self.search_url = self.response.html.find("a#pagination-next")[0].absolute_links.pop()
            else:
                self.search_url = ""

    def _get(self):
        self.session.headers['User-Agent'] = self.ua.random
        time.sleep(uniform(2, 4))
        self.response = self.session.get(self.search_url)

    def _save_urls(self):
        for url in self.add_list:
            add = Annonce()
            add.lien = url
            try:
                add.save()
            except:
                pass


class LoadData():
    def __init__(self, search_url):
        self.search_url = search_url
        self.session = HTMLSession()
        self.ua = UserAgent()
        self._get()
        self._parse()
        self._save_datas()

    def _parse(self):
        self.data = {
            'titre': self.response.html.find("h1.item-title")[0].text.replace("\xa0", ""),
            'prix': int(self.response.html.find("span.item-price")[0].text.split("\xa0")[0].replace(".", "")),
            'surface': int([e for e in self.response.html.find("strong") if "m²" in e.text][0].text.split("\xa0")[0]),
            'description': self.response.html.find("div.item-description div p")[0].text,
            'code_postal': self.response.html.find("h1.item-title")[0].text.split("(")[1].split(")")[0],
            #'date_publication': datetime.strptime(self.response.html.find("p.item-date")[0].text.split("/")[-1].strip(),
            #                                      "%d %B %Y"),
            'status': 'VALIDE'
        }

    def _get(self):
        self.session.headers['User-Agent'] = self.ua.random
        time.sleep(uniform(2, 4))
        self.response = self.session.get(self.search_url)

    def _save_datas(self):
        try:
            print(self.data)
            Annonce.objects.filter(lien=self.search_url).update(**self.data)
        except:
            Annonce.objects.filter(lien=self.search_url).update(status='ERREUR')