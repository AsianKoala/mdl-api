from scrapers.scrape import IDScraper, Options
from scrapers.parse import DramaParser

scraper = IDScraper(force_refresh_cache=False)
opts = Options(dramas=True)
parser = DramaParser("1814-always")


def parse_search():
    search_url = "https://mydramalist.com/search?adv=titles&ty=68,86&re=1890,2023&so=newest&or=desc&page=1"
    false_url = "https://mydramalist.com/search?adv=titles&ty=68&re=1890,2001&so=newest&or=desc&page=250"
    print(scraper.new_items)

def get_year_ids():
    scraper.scrape_year_ids(2003, opts, page_end=2, sleep_sec=0.2)
    # parser.write_cache()

def drama_parser():
    model = parser.parse_model()
    print(model)

drama_parser()
