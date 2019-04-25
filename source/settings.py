QUERY_INSERT_STOCK_PRICE = '''
    INSERT INTO equity_data.closing_prices
    (uuid, ticker, adjusted_close_price, trading_date)
    VALUES
    (%(uuid)s, %(ticker)s, %(adjusted_close_price)s, %(trading_date)s)
    ON CONFLICT DO NOTHING;
    '''

QUERY_GET_TICKERS = '''
with open_positions as (
	select
		instrument,
		max(num_open_positions) as num_open_positions
	from robinhood.open_positions
	group by 1
	),

final_data as (

select
	t.symbol,
	max(t.full_name) as full_name,
	max(t.list_date) as list_date,
	max(t.country) as country,
	sum(t2.num_open_positions) as num_open_positions
from robinhood.instrument_details as t
left join open_positions as t2 on t2.instrument = t.url
where url in (select instrument from open_positions)
group by t.symbol
order by num_open_positions desc
)

select symbol
from final_data
where num_open_positions > 1000;
'''
