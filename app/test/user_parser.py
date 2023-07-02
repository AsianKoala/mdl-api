from scrapers.watchlist import WatchlistParser


def main():
    scraper = WatchlistParser()
    scraper.scrape("koawa")
    scraper.parse_model()


if __name__ == "__main__":
    main()
