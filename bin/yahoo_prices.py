import datetime
import requests
import sys

sys.path.append("../source")

import private
import settings
import utils


def get_ticker_data(ticker, run_id):
    url = settings.URL_YAHOO_CHART.format(ticker=ticker, run_id=run_id)
    response = requests.get(url)
    data = response.json()['chart']['result'][0]

    return data

def convert_to_date(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

def parse_stock_prices(data):
    prices = data['indicators']['adjclose'][0]['adjclose']
    trading_dates = [convert_to_date(timestamp) for timestamp in data['timestamp']]
    uuids = [utils.generate_uuid() for i in range(len(prices))]
    symbol = [data['meta']['symbol'] for i in range(len(prices))]
    stock_prices = zip(uuids, symbol, prices, trading_dates)

    return stock_prices

def filter_existing_dates(stock_prices, existing_dates):
    return [data for data in stock_prices if data[3] not in existing_dates]


if __name__ == '__main__':
    run_id = utils.generate_run_id()
    tickers = utils.get_list_from_db(settings.QUERY_GET_TICKERS)

    for ticker in tickers:
        print(ticker)
        try:
            data = get_ticker_data(ticker, run_id)
            stock_prices = parse_stock_prices(data)
            existing_dates = utils.get_list_from_db(settings.QUERY_GET_TRADING_DATES.format(ticker))
            new_data = filter_existing_dates(stock_prices, existing_dates)

            utils.write_many_to_database(new_data, settings.QUERY_INSERT_STOCK_PRICES)
        except Exception as e:
            print(e)
