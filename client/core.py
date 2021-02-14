import time
from random import uniform

from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
import requests
from requests_html import HTMLSession


def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate("my_password")
        controller.signal(Signal.NEWNYM)


class TorClient:
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    ua = UserAgent()
    headers = requests.utils.default_headers()
    session = HTMLSession()

    def get(self, url):
        change_ip()
        self._set_ua()
        time.sleep(uniform(3, 5))
        return self.session.get(
            url,
            proxies=self.proxies,
            headers=self.headers,
        )

    def _set_ua(self):
        self.headers['User-Agent'] = self.ua.random
