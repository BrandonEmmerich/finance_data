QUERY_INSERT_STOCK_PRICES = '''
    INSERT INTO equity_data.closing_prices
    (uuid, ticker, adjusted_close_price, trading_date)
    VALUES
    %s
    '''

QUERY_INSERT_STOCK_DETAILS = '''
    INSERT INTO equity_data.iex_details
    (uuid, date_added, run_id, symbol, company_name, marketcap,
    beta, institution_percent, price_to_book, price_to_sales)
    VALUES
    (%(uuid)s, %(date_added)s, %(run_id)s, %(symbol)s, %(company_name)s, %(marketcap)s,
    %(beta)s, %(institution_percent)s, %(price_to_book)s, %(price_to_sales)s)
    '''

QUERY_INSERT_SP_CONSTITUENTS = '''
    INSERT INTO equity_data.sp_constituents
    (uuid, run_id, date_added, full_name, sector, symbol)
    VALUES
    %s
    '''

QUERY_GET_TRADING_DATES = 'select trading_date from equity_data.closing_prices where ticker = \'{}\''

QUERY_GET_TICKERS = '''select symbol from equity_data.sp_constituents'''

QUERY_GET_TICKERS_FOR_IEX = '''
    select symbol
    from (
    	select
    		t.date_added,
    		num_open_positions,
    		full_name,
    		symbol
    	from robinhood.open_positions as t
    	left join robinhood.instrument_details as t2 on t.instrument = t2.url
    	where t.run_id = (select max(run_id) from robinhood.open_positions)
    	) as foo;
    '''

URL_YAHOO_CHART = 'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}L?symbol={ticker}&period1=1280914000&period2={run_id}&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=YsvQxyK%2Fz6I&corsDomain=finance.yahoo.com'
