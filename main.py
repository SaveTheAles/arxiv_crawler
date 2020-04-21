from scrapper import *
from tx_generator import *
from config import *
import arxiv
import json
from progressbar import Bar, ETA, FileTransferSpeed, Percentage, ProgressBar

widgets = ['Progress: ', Percentage(), ' ',
               Bar(marker='-',left='[',right=']'),
               ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=500)

results = arxiv.query(query=QUERY, max_chunk_results=10, iterative=True)

print('Collecting articles by', QUERY, 'keyword and generating transactions for broadcasting.')
i = 0
for result in pbar(results()):
    df = create_clinks_set(result, DATA_PATH)
    tx = tx_generator(df, 'quantum computing article')
    with open(TXS_PATH + '/link_tx{}.json'.format(i), 'w') as outfile:
        json.dump(tx, outfile)
    i+=1
