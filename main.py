from helper import *
from config import *
import arxiv

results = arxiv.query(query=QUERY, max_chunk_results=100, iterative=True)

account = {
    "address": ADDRESS,
    "account_number": str(getAccountNumber(ADDRESS)),
    "public_key": getPubKey(ADDRESS),
    "sequence": getSequence(ADDRESS)
}

print('Signing and broadcasting txs by', QUERY, 'keyword ')
i = 0
for result in results():
    print('Try to create cyberlink set for tx #{}'.format(i))
    df = createClinksSet(ADDRESS, result)
    if df.empty:
       pass
    else:
        sequence = getSequence(ADDRESS)
        tx_generator(df, i, account)
        sign(i, account)
        broadcast(i)
        account['sequence'] += 1
    i += 1

