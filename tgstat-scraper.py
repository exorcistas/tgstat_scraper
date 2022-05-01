import argparse
from proxylist import ProxyList
import requests
from bs4 import BeautifulSoup


#BASE_URL = "https://tgstat.com/search"
BASE_URL = "https://tgstat.ru/en/search"


""" PROXY FUNCTIONS """
def loadProxyList():
    proxylist = ProxyList()
    print(f"Fetching proxy list...")
    proxylist.load_url("https://github.com/jetkai/proxy-list/raw/main/online-proxies/txt/proxies-http.txt")
    return proxylist

def getRandomProxy(proxylist):
    proxy = proxylist.random().address()
    print(f"Using proxy: {proxy}")
    return proxy


""" TGSTAT FUNCTIONS """
def parseResponse(response, xpath):
    channels = []
    if (response.status_code == 200):
        soup = BeautifulSoup(response.content, "html.parser")
        repost_channels = soup.find_all("a", attrs={"class": xpath})
        channels += [x["href"] for x in repost_channels if "http" in x["href"]]
    else:
        raise(f"Return status not OK: {response.status_code}")
    return channels

def filterUniqueChannels(channels):
    channels = list(set(channels))
    print(str(len(channels)) + " unique channels found:")
    for url in channels:
        print(url)
    return channels

def getRelatedChannels(url):
    proxies = { 'http': getRandomProxy(PROXY_LIST) }
    resp = requests.get(url, proxies=proxies)
    channels = parseResponse(resp, "ellipsis-link")
    channels = filterUniqueChannels(channels)
    return channels

def searchChannels(keywords):
    headers = {'content-type': "application/x-www-form-urlencoded"}
    post_data = {"q": f"""{keywords}"""}
    proxies = { 'http': getRandomProxy(PROXY_LIST) }
    channels = []    

    print(f"Searching with keywords: '{keywords}'")
    resp = requests.post(BASE_URL, headers=headers, data=post_data, proxies=proxies)
    channels = parseResponse(resp, "channel-post-title")
    channels = filterUniqueChannels(channels)
    return channels


""" MAIN """
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="search channels by phrase", type=str)
    parser.add_argument("-u", "--url", help="channel URL to get related channels", type=str)
    parser.add_argument("-o", "--output", help="text output file", type=str)
    args = parser.parse_args()

    if ((args.search and args.url) or (not args.search and not args.url)):
        raise("Bad arguments, call -h for help")

    PROXY_LIST = loadProxyList()
    if (args.search and not args.url):
        channels = searchChannels(args.search)

    elif (not args.search and args.url):
        channels = getRelatedChannels(args.url)

    if (args.output):
        with open(args.output, 'w') as fp:
            fp.write("\n".join(channels))