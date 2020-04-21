#!/bin/bash
for (( i=421; i <= 489; i++ ))
do
echo "at $i tx"
cyberdcli tx sign ./data/txs/link_tx$i.json --from ales --output-document ./data/txs/link_txs$i.json --chain-id euler-6 --node http://moon.cybernode.ai:36657
cyberdcli tx broadcast ./data/txs/link_txs$i.json --node http://moon.cybernode.ai:36657
sleep 7
done