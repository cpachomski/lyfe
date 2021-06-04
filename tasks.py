from __future__ import absolute_import, unicode_literals

import os
import logging
from celery import Celery
import stonks.robinhood as rh
import news.nyt as nyt
import news.theguardian as theguardian

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lyfe.settings")

app = Celery("lyfe")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.00*10.00, refresh_news_sections.s())
    sender.add_periodic_task(30.00, refresh_rh_data.s())


@app.task
def refresh_news_sections():
    sections = ['world', 'football', 'sports', 'home', 'arts', 'business', 'science', 'travel']
    for section in sections:
        nyt.cache_section(section)
        theguardian.cache_section(section)


@app.task
def refresh_rh_data():
    rh.cache_user_profile()
    rh.cache_stocks(rh.get_user_stocks())
    rh.cache_open_option_positions()
