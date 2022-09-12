from .settings import PROXY_LIST
from .proxy import get_random_proxy
import requests
import requests_random_user_agent
from bs4 import BeautifulSoup


class TgStatScraper:
    def __init__(self, proxy_list: list = []):
        #self._base_url = "https://tgstat.com/search"
        self._base_url = "https://tgstat.ru/en/search"
        self._proxy_list = proxy_list

    @classmethod
    def from_settings(cls):
        return cls(PROXY_LIST)

    def _get_random_proxy(self):
        return get_random_proxy(self._proxy_list)

    def _parse_response(self, response, xpath):
        channels = []
        if (response.status_code == 200):
            soup = BeautifulSoup(response.content, "html.parser")
            repost_channels = soup.find_all("a", attrs={"class": xpath})
            channels += [x["href"] for x in repost_channels if "http" in x["href"]]
        else:
            raise ValueError(f"Return status not OK: {response.status_code}")
        return channels

    def _filter_unique_channels(self, channels):
        channels = list(set(channels))
        print(str(len(channels)) + " unique channels found:")
        for url in channels:
            print(url)
        return channels

    def get_related_channels(self, url):
        proxies = { 'all://': self._get_random_proxy() }
        resp = requests.get(url, proxies=proxies)
        channels = self._parse_response(resp, "ellipsis-link")
        channels = self._filter_unique_channels(channels)
        return channels

    def search_channels(self, keywords):
        headers = {'content-type': "application/x-www-form-urlencoded"}
        post_data = {"q": f"""{keywords}"""}
        proxies = { 'all://': self._get_random_proxy() }
        channels = []    

        print(f"Searching with keywords: '{keywords}'")
        resp = requests.post(self._base_url, headers=headers, data=post_data, proxies=proxies)
        channels = self._parse_response(resp, "channel-post-title")
        channels = self._filter_unique_channels(channels)
        return channels
