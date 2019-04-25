import datetime
import requests
import sys

sys.path.append("../source")

import private
import settings
import utils


def get_ticker_data(ticker, run_id):
    url_base = 'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}L?symbol={ticker}&period1=1280914000&period2={run_id}&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=YsvQxyK%2Fz6I&corsDomain=finance.yahoo.com'.format(ticker=ticker, run_id=run_id)
    response = requests.get(url_base)
    data = response.json()['chart']['result'][0]

    return data

def convert_to_date(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

def parse_stock_prices(data):
    prices = data['indicators']['adjclose'][0]['adjclose']
    timestamps = data['timestamp']
    stock_prices = zip(timestamps, prices)

    return stock_prices

if __name__ == '__main__':
    run_id = utils.generate_run_id()
    tickers = utils.get_list_from_db(settings.QUERY_GET_TICKERS)

    for ticker in tickers:
        print(ticker)
        data = get_ticker_data(ticker, run_id)
        stock_prices = parse_stock_prices(data)

        for timestamp, price in stock_prices:
            row = {
                'ticker': ticker,
                'trading_date': convert_to_date(timestamp),
                'adjusted_close_price': price,
                'uuid': ticker + '_' + str(convert_to_date(timestamp))
            }
            utils.write_to_database(row, settings.QUERY_INSERT_STOCK_PRICE)
