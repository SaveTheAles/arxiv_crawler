import pandas as pd
from multi_rake import Rake
import ipfshttpclient
from config import *
import arxiv

client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
rake = Rake()

def create_clinks_set(item, dirpath):
    paper = {'pdf_url': item['pdf_url'], "title": item['title']}
    summary = item['summary']
    title = item['title']
    summary = title + '. ' + summary

    keywords = rake.apply(summary)
    path = arxiv.download(paper, dirpath=dirpath)

    cid_to = client.add(path)['Hash']
    cid_from_list = []

    for keyword in keywords:
        if keyword[1] > RANK:
            temp = client.add_str(keyword[0])
            cid_from_list.append(temp)
        else:
            pass

    cid_from_list.append(client.add_str(title))

    data = {'title': title, 'cid_from': cid_from_list, 'cid_to': cid_to}

    clinks_df = pd.DataFrame.from_dict(data)
    return clinks_df