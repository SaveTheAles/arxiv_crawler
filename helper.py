import pandas as pd
from multi_rake import Rake
import ipfshttpclient
import arxiv
from config import *
import os
import requests
import json

# Check if you have linked this hash already
def ifLinkExists(address, cid):
    request = requests.get(LCD_API+'/txs?cyberlink.objectTo={}&cybermeta.subject={}&limit=1'.format(cid, address))
    if (request.status_code == 200):
        if (request.json()['txs'] !=[]):
            ifExists = True
        else:
            ifExists = False
    return ifExists

# Create ipfs http connection to API
def createIPFSClient():
    return ipfshttpclient.connect(IPFS_HTTP_CLIENT)

# Get summary about article with title
def getSummary(item):
    summary = item['summary']
    title = item['title']
    summary = title + '. ' + summary
    return summary

# Get list of keywords from the text
def getKeyWords(text):
    rake = Rake()
    keywords = rake.apply(text)
    sortedKw = []
    for keyword in keywords:
        if keyword[1] > RANK:
            sortedKw.append(keyword[0])
        else:
            pass
    return sortedKw

# Download article pdf to dirpath
def downloadArticle(item, dirpath):
    paper = {'pdf_url': item['pdf_url'], "title": item['title']}
    path = arxiv.download(paper, dirpath=dirpath)
    return path

def getFileHash(path):
    client = createIPFSClient()
    cid = client.add(path)['Hash']
    return cid

def getStringHash(string):
    client = createIPFSClient()
    cid = client.add_str(string)
    return cid

def removeFile(path):
    os.remove(path)

def tx_generator(df, i, account):
    msgs = []
    for index, row in df.iterrows():
        msg = {
            "type": "cyber/Link",
            "value": {
                "address": account['address'],
                "links": [
                    {
                        "from": row['cid_from'],
                        "to": row['cid_to']
                    }
                ]
            }
        }
        msgs.append(msg)
    links_tx = {
        "type": "cosmos-sdk/StdTx",
        "value": {
            "msg": msgs,
            "fee": {
                "amount": [],
                "gas": "0"
            },
            "signatures": None,
            "memo": MEMO
        }
    }
    with open(TXS_PATH + '/link_tx{}.json'.format(i), 'w') as outfile:
        json.dump(links_tx, outfile)

def createClinksSet(address, item):
    path = downloadArticle(item, DATA_PATH)
    hash = getFileHash(path)
    if(ifLinkExists(address, hash)):
        removeFile(path)
        print('you have cyberlinked', hash, 'already')
        clinks_df = pd.DataFrame()
    else:
        cid_to = hash
        cid_from_list = []
        (getStringHash(item['title']))
        cid_from_list.append(getStringHash(QUERY))
        kws = getKeyWords(item['summary'])
        for kw in kws:
            cid_from_list.append(getStringHash(kw))
        data = {'title': item['title'], 'cid_from': cid_from_list, 'cid_to': cid_to}
        clinks_df = pd.DataFrame.from_dict(data)
    return clinks_df

def sign(i, account):
    os.system(
        'cyberdcli tx sign ./data/txs/link_tx{}.json --from {} --output-document {}/link_txs{}.json --chain-id euler-6 --node {} --sequence {}'.format(
            i, ACCOUNT, TXS_PATH, i, PROXY_NODE, account['sequence']))

def broadcast(i):
    os.system('cyberdcli tx broadcast {}/link_txs{}.json --node {}'.format(TXS_PATH, i, PROXY_NODE))

def getSequence(address):
    request = requests.get(LCD_API+'/auth/accounts/{}'.format(address))
    return request.json()['result']['value']['sequence']

def getAccountNumber(address):
    request = requests.get(LCD_API+'/auth/accounts/{}'.format(address))
    return request.json()['result']['value']['account_number']

def getPubKey(address):
    request = requests.get(LCD_API+'/auth/accounts/{}'.format(address))
    return request.json()['result']['value']['public_key']