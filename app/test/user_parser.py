import requests


def main():
    # scraper = WatchlistParser()
    # scraper.scrape("koawa")
    # scraper.parse_model()

    r = requests.get("https://mydramalist.com/35729-emergency-lands-of-love/cast")

    with open("app/.cache/cast.html", "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    main()
