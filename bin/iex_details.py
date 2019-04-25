import requests
import sys

sys.path.append("../source")

import private
import settings
import utils


def get_ticker_data(ticker):
    url = 'https://api.iextrading.com/1.0/stock/{}/stats'.format(ticker)
    response = requests.get(url)
    return response.json()

def parse_details(data):
    row = {
        'symbol': data['symbol'],
        'company_name': data['companyName'],
        'marketcap': data['marketcap'],
        'beta': data['beta'],
        'institution_percent': data['institutionPercent'],
        'price_to_sales': data['priceToSales'],
        'price_to_book': data['priceToBook'],
    }
    return row

if __name__ == '__main__':
    date_added = utils.right_now()
    run_id = utils.generate_run_id()
    tickers = utils.get_list_from_db(settings.QUERY_GET_TICKERS_FOR_IEX)

    for ticker in tickers:
        print(ticker)
        try:
            data = get_ticker_data(ticker)
            row = parse_details(data)
            bundled_data = utils.bundled_data(date_added, run_id)
            row.update(bundled_data)
            utils.write_to_database(row, settings.QUERY_INSERT_STOCK_DETAILS)
        except Exception as e:
            print(e)

    import ipdb; ipdb.set_trace()
