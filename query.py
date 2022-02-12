from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import json
from helper import get_pair_id, get_token_id, get_trade_id

sample_transport=RequestsHTTPTransport(
    url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
    verify=True,
    retries=3,
)

client = Client(
    transport=sample_transport
)

possible_uni_id = get_token_id(client, 'UNI')
possible_weth_id = get_token_id(client, 'WETH')
print('UNI ID: ', possible_uni_id, '\nWETH ID: ', possible_weth_id)

possible_pair_id = get_pair_id(client, possible_uni_id, possible_weth_id)
print('UNI-WETH Pair ID: ', possible_pair_id)

trade_ids = get_trade_id(client, possible_pair_id)
print('Trade ID: ', trade_ids)

# Save response JSON to file
with open('response.json', 'w') as outfile:
    json.dump(trade_ids, outfile)