from config import ADDRESS

def tx_generator(df, memo):
    msgs = []
    for index, row in df.iterrows():
        cid_from = row['cid_from']
        cid_to = row['cid_to']
        msg = {
            "type": "cyber/Link",
            "value": {
                "address": ADDRESS,
                "links": [
                    {
                        "from": cid_from,
                        "to": cid_to
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
            "memo": memo
        }
    }
    return links_tx