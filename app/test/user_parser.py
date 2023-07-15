import requests
from scrapers.drama import DramaParser


def main():
    # scraper = WatchlistParser()
    # scraper.scrape("koawa")
    # scraper.parse_model()

    scraper = DramaParser()
    scraper.parse_directors(None)


if __name__ == "__main__":
    main()
