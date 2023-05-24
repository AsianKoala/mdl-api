from scrape import Parser

parser = Parser(force_refresh_cache=False)
opts = Parser.Options(dramas=True)
# parser.get_year_ids(year=2023, opts=opts)


def parse_search():
    search_url = "https://mydramalist.com/search?adv=titles&ty=68,86&re=1890,2023&so=newest&or=desc&page=1"
    false_url = "https://mydramalist.com/search?adv=titles&ty=68&re=1890,2001&so=newest&or=desc&page=250"
    print(parser.new_items)

def get_year_ids():
    parser.get_year_ids(2003, opts, page_end=2, sleep_sec=0.2)
    # parser.write_cache()

get_year_ids()

