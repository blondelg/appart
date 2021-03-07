import time
from fake_useragent import UserAgent
import requests
from requests_html import HTMLSession
from stem import Signal
from stem.control import Controller
from pythonping import ping
import re


def get_tor_container_ip():
    return re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(ping("tor")))[0]

def rotate():
    with Controller.from_port(address=f"{get_tor_container_ip()}", port=9051) as controller:
        controller.authenticate(password="bonjour")
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
    return

class TorClient:
    proxies = {
        'http': 'socks5://tor:9050',
        'https': 'socks5://tor:9050'
    }
    ua = UserAgent(use_cache_server=False, verify_ssl=False)
    headers = requests.utils.default_headers()
    session = HTMLSession()

    def get(self, url):
        rotate()
        self._set_ua()
        return self.session.get(
            url,
            proxies=self.proxies,
            headers=self.headers,
        )

    def _set_ua(self):
        self.headers['User-Agent'] = self.ua.random