import os
import pyotp
import logging
import robin_stocks.robinhood as rh
from lyfe.fetch import cache, get_one, get_all

logger = logging.getLogger(__name__)
cache_key_prefix = "rh-"

# login to Robinhood with multi-factor auth
totp = pyotp.TOTP(os.environ.get("RH_2FA_KEY")).now()
rh.login(os.environ.get("RH_USERNAME"), os.environ.get("RH_PASSWORD"), mfa_code=totp)


def cache_user_profile():
    profile = rh.account.build_user_profile()
    holdings = rh.account.build_holdings()
    cache(f"{cache_key_prefix}user_profile", profile | {"holdings": holdings})


def cache_stocks(symbols):
    stocks = rh.stocks.get_fundamentals(symbols)
    for stock in stocks:
        sym = stock["symbol"]
        cache(f"{cache_key_prefix}{sym.lower()}", stock)


def cache_open_option_positions():
    key = f"{cache_key_prefix}options-positions"
    positions = rh.options.get_open_option_positions()
    cache(key, positions)


def get_user_profile():
    return get_one(f"{cache_key_prefix}user_profile")


def get_user_stocks():
    profile = get_user_profile()
    return list(profile["holdings"].keys()) + ['BB', 'AMC']


def get_stocks(symbols):
    keys = [f"{cache_key_prefix}{s.lower()}" for s in symbols]
    return get_all(keys)


def get_open_option_positions():
    return get_one(f"{cache_key_prefix}options-positions")