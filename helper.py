from typing import List
from gql import gql, Client


def get_token_id(client: Client, token_symbol: str) -> str:
    query = gql('''
    query {
        tokens (where: {symbol: "%s"}) {
            id
        }
    }
    ''' % token_symbol
                )

    response = client.execute(query)
    return response['tokens']


def get_pair_id(client: Client, possible_token0_id: List[str], possible_token1_id: List[str]) -> str:
    possible_pair_id = []
    for token0 in possible_token0_id:
        for token1 in possible_token1_id:
            pair_id = get_pair_id_helper(
                client, token0['id'], token1['id'])

            for id in pair_id:
                possible_pair_id.append(id)

    return possible_pair_id


def get_pair_id_helper(client: Client, token0_id: str, token1_id: str) -> str:
    query = gql('''
    query {
        pairs (where: {token0: "%s", token1: "%s"}) {
            id
        }
    }
    ''' % (token0_id, token1_id)
    )

    response = client.execute(query)
    return response['pairs']


def get_trade_id(client: Client, possible_pair_id: List[str]) -> str:
    possible_trade_id = []
    for id in possible_pair_id:
        trade_id = get_trade_id_helper(client, id['id'])
        for id in trade_id:
            possible_trade_id.append(id)

    return possible_trade_id


def get_trade_id_helper(client: Client, pair_id: str) -> str:
    query = gql('''
    query trades{
        swaps(where:{pair: "%s"}, orderBy: timestamp, orderDirection: desc) {
            id
            timestamp
            amount0In
            amount1In
            amount0Out
            amount1Out
            pair {
                token0 {
                    id
                    symbol
                }
                token1 {
                    id
                    symbol
                }
            }
            transaction {
                blockNumber
            }
        }
    }
    ''' % pair_id
                )

    response = client.execute(query)
    return response['swaps']
