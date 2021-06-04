from django.http import JsonResponse
import stonks.robinhood as rh


def stonks_index(request):
    symbols = rh.get_user_stocks()
    options = rh.get_open_option_positions()
    stocks = rh.get_stocks(symbols)
    data = {"stocks": stocks, "options": options}
    return JsonResponse(data, safe=False)
