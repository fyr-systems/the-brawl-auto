# The Brawl trading API guide
Enabling algorithmic trading on The Brawl platform

## Transaction request

### POST http://platform.the-brawl.eu/api/transaction
#### Request body: {

`sourceWalletId`: Source wallet ID available from the UI (see below)

`destWalletId`: Destination wallet ID available from the UI (see below)

`amountFromSourceWallet`: [excludable with `amountToDestWallet`] Number of the currency units to sell from the source wallet

`amountToDestWallet`: [excludable with `amountFromSourceWallet`] Number of the currency units to buy

`exchangeRate`: [*OPTIONAL*] Transaction will be rejected if set exchange rate is worse at the moment of execution (it's always the rate *DESTINATION_CURRENCY/SOURCE_CURRENCY*, see examples below)

#### }

#### Header:

`Authorization`: `Bearer <id_token>` (see Python code example)

## Where to find wallet IDs
![Wallet IDs](wallet-ids.png "Where to find wallet IDs")

## Alternatively, where to find wallet ID (from URL or UI)
![Wallet ID](wallet-id.png "Alternatively, where to find wallet ID")

## Examples
### Buying BTC for 10 USD
POST http://platform.the-brawl.eu/api/transaction \
Request body: { \
`sourceWalletId`: `<USD_wallet_ID>` \
`destWalletId`: `<BTC_wallet_ID>` \
`amountFromSourceWallet`: 10 \
`exchangeRate`: `<requested_exchange_rate_boundary> [BTC/USD rate]` \
}

### Buying 5 BTC for USD
POST http://platform.the-brawl.eu/api/transaction \
Request body: { \
`sourceWalletId`: `<USD_wallet_ID>` \
`destWalletId`: `<BTC_wallet_ID>` \
`amountToDestWallet`: 5 \
`exchangeRate`: `<requested_exchange_rate_boundary> [BTC/USD rate]` \
}

### Buying USD for 20 ETH
POST http://platform.the-brawl.eu/api/transaction \
Request body: { \
`sourceWalletId`: `<ETH_wallet_ID>` \
`destWalletId`: `<USD_wallet_ID>` \
`amountFromSourceWallet`: 20 \
`exchangeRate`: `<requested_exchange_rate_boundary> [USD/ETH rate]` \
}

### Buying 15 USD for ETH
POST http://platform.the-brawl.eu/api/transaction \
Request body: { \
`sourceWalletId`: `<ETH_wallet_ID>` \
`destWalletId`: `<USD_wallet_ID>` \
`amountToDestWallet`: 15 \
`exchangeRate`: `<requested_exchange_rate_boundary> [USD/ETH rate]` \
}

## Example code
**In order to run the example code, you need to set the `THE_BRAWL_EMAIL` and `THE_BRAWL_PASSWORD` environment variables with your login credentials to The Brawl platform. You can see the `export THE_BRAWL_EMAIL=<your_email>` and `export THE_BRAWL_PASSWORD=<your_password>` commands in BASH.**

[example.py](example.py)
```python
from os import environ
import requests

API_KEY = 'AIzaSyBOEvN4OzAePlFp1fSRKWJlioA9r2WPZHw'
AUTH_URL = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
TRANSACTION_URL = 'http://platform.the-brawl.eu/api/transaction'

data = {
    "email": environ['THE_BRAWL_EMAIL'],
    "password": environ['THE_BRAWL_PASSWORD'],
    "returnSecureToken": True,
}
res = requests.post(AUTH_URL, json=data, params={'key': API_KEY}).json()
id_token = res['idToken']

res = requests.post(TRANSACTION_URL, headers={
    'Authorization': f'Bearer {id_token}'
}, json={
    "sourceWalletId": '1d0e3ee6-1fac-4246-a869-9c383ae8fa9c',
    "destWalletId": '030bcff8-1bde-4b89-b814-b9c75cfda896',
    "amountFromSourceWallet": 10,
    "exchangeRate": 2.2,
}, verify=False)
```

## Note
In order to get the information about exchange rates, you need to integrate in your algorithm a data source like [CoinBase](https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs) or [CoinGecko](https://www.coingecko.com/api/documentation).
