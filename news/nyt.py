import os
import logging
from lyfe.fetch import fetch_and_cache, get_one
from dateutil import parser

logger = logging.getLogger(__name__)

api_key = os.environ.get("NYT_API_KEY")
cache_key_prefix = "nyt-"


def normalize_results(story):
    return {
        "source": "NYT",
        "source_logo": "https://developer.nytimes.com/files/poweredby_nytimes_30a.png?v=1583354208339",
        "section": story["section"],
        "subsection": story.get("subsection"),
        "headline": story["title"],
        "byline": story["byline"],
        "url": story["short_url"],
        "images": story["multimedia"],
        "last_updated": parser.parse(story["updated_date"]),
    }


def cache_section(section):
    fetch_and_cache(
        f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}",
        f"{cache_key_prefix}{section}"
    )


def get_section(section):
    try:
        cached = get_one(f"{cache_key_prefix}{section}")
        if cached.get('results'):
            return list(map(normalize_results, cached["results"]))
    except Exception:
        logger.warn("Cannot get NYT section -> {}", section)
        return []

