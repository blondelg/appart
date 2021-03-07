from annonces.models import Annonce
from datetime import date
import time

from client.core import TorClient

mois = {
    'janvier':1,
    'février':2,
    'mars':3,
    'avril':4,
    'mai':5,
    'juin':6,
    'juillet':7,
    'aout':8,
    'août':8,
    'septembre':9,
    'octobre':10,
    'novembre':11,
    'décembre':12,
}

class GetUrls():
    def __init__(self, search_url):
        self.search_url = search_url
        self.session = TorClient()
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
        self.session = TorClient()
        self._get()
        self._save_datas()

    def _parse(self):
        temp_date = self.response.html.find("p.item-date")[0].text.split("/")[-1].strip().split(" ")
        temp_date[1] = mois[temp_date[1]]
        temp_date = [int(i) for i in temp_date]
        self.data = {
            'titre': self.response.html.find("h1.item-title")[0].text.replace("\xa0", ""),
            'prix': int(self.response.html.find("span.item-price")[0].text.split("\xa0")[0].replace(".", "")),
            'surface': int([e for e in self.response.html.find("strong") if "m²" in e.text][0].text.split("\xa0")[0]),
            'description': self.response.html.find("div.item-description div p")[0].text,
            'code_postal': self.response.html.find("h1.item-title")[0].text.split("(")[1].split(")")[0],
            'date_publication': date(temp_date[2], temp_date[1], temp_date[0]),
            'status': 'VALIDE'
        }

    def _get(self):
        self.response = self.session.get(self.search_url)

    def _save_datas(self):
        try:
            self._parse()
            Annonce.objects.filter(lien=self.search_url).update(**self.data)
            print("SAVE ANNONCE OK ", self.data['titre'])
        except:
            Annonce.objects.filter(lien=self.search_url).update(status='ERREUR')
            print("SAVE ANNONCE ERROR ", self.data['titre'])