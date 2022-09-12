from proxylist import ProxyList


def load_proxy_list(url: str = "") -> ProxyList:
    proxylist = ProxyList()
    #proxylist.load_file(file_path)
    if url: proxylist.load_url(url)
    return proxylist

def get_random_proxy(proxylist: ProxyList):
    try:
        proxy = str(proxylist.random().address())
    except ValueError:
        print("Proxy list empty")
        proxy = ""
    return proxy
    