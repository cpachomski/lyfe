import os
import logging
from lyfe.fetch import fetch_and_cache, get_one
from dateutil import parser

logger = logging.getLogger(__name__)

api_key = os.environ.get('GUARDIAN_API_KEY')
cache_key_prefix = "guardian-"


def normalize_results(story):
    return {
        "source": "THE GUARDIAN",
        "source_logo": "https://assets.guim.co.uk/images/apps/app-logo.png",
        "section": story["sectionId"],
        "subsection": story.get("subsection"),
        "headline": story["webTitle"],
        "url": story["webUrl"],
        "last_updated": parser.parse(story["webPublicationDate"]),
    }


def cache_section(section):
    fetch_and_cache(
        f"https://content.guardianapis.com/{section}?api-key={api_key}",
        f"{cache_key_prefix}{section}"
    )


def get_section(section):
    try:
        cached = get_one(f"{cache_key_prefix}{section}")
        if cached.get('response'):
            return list(map(normalize_results, cached["response"]["results"]))
    except Exception:
        logger.warn("Cannot get Guardian section -> {}", section)
        return []
