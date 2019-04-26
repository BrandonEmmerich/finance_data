import requests
import sys

sys.path.append("../source")

import private
import settings
import utils

def parse_to_tuples(data):
    tuples = []
    for d in data:
        _tuple = (utils.generate_uuid(), run_id, date_added, d['Name'], d['Sector'], d['Symbol'])
        tuples.append(_tuple)

    return tuples

if __name__ == '__main__':
    run_id = utils.generate_run_id()
    date_added = utils.right_now()

    url = 'https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json'
    data = utils.get_response_json(url)
    tuples = parse_to_tuples(data)
    utils.write_many_to_database(tuples, settings.QUERY_INSERT_SP_CONSTITUENTS)
