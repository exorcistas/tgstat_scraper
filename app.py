import argparse
from tgstat_scraper import TgStatScraper


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--search", help="search channels by phrase", type=str)
        parser.add_argument("-u", "--url", help="channel URL to get related channels", type=str)
        parser.add_argument("-o", "--output", help="text output file", type=str)
        args = parser.parse_args()

        if ((args.search and args.url) or (not args.search and not args.url)):
            raise ValueError("Bad arguments, call -h for help")

    
        tgstat = TgStatScraper.from_settings()
        if (args.search and not args.url):
            channels = tgstat.search_channels(args.search)

        elif (not args.search and args.url):
            channels = tgstat.get_related_channels(args.url)

        if (args.output):
            with open(args.output, 'w') as fp:
                fp.write("\n".join(channels))
    
    except Exception as ex:
        if '403' in str(ex):
            print("Random proxy has been blocked. Try again.")
        else:
            print(f"{type(ex).__name__}: {ex}")


if __name__ == "__main__":
    main()
