import news.nyt as nyt
import news.theguardian as theguardian
from django.shortcuts import render
import stonks.robinhood as rh


def section_index(request, section_name):
    # get news
    nyt_stories = nyt.get_section(section_name)
    guardian_stories = theguardian.get_section(section_name)
    stories = []
    for st in [nyt_stories, guardian_stories]:
        if st:
            stories = stories + st

    # get stonks
    symbols = rh.get_user_stocks()
    stocks = rh.get_stocks(symbols)
    options = rh.get_open_option_positions()

    context = {"stories": stories, "stocks": stocks, "options": options}
    return render(request, "article-list.html", context)
