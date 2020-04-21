from scrapper import *
from tx_generator import *
from config import *
import arxiv
import json

results = arxiv.query(query=QUERY, max_results=2)

i = 0
for result in results:
    df = create_clinks_set(result, DATA_PATH)
    tx = tx_generator(df, 'quantum computing article')
    with open(TXS_PATH + '/link_tx{}.json'.format(i), 'w') as outfile:
        json.dump(tx, outfile)
    i+=1
