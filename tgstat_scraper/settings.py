from .proxy import load_proxy_list


PROXY_LIST_URL = "https://github.com/jetkai/proxy-list/raw/main/online-proxies/txt/proxies-http.txt"
PROXY_LIST = load_proxy_list(url=PROXY_LIST_URL)
