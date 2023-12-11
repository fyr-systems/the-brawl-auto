from os import environ
import requests

API_KEY = 'AIzaSyBOEvN4OzAePlFp1fSRKWJlioA9r2WPZHw'
AUTH_URL = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
TRANSACTION_URL = 'http://platform.the-brawl.eu/api/transaction'
ACCOUNT_ID = 'f24802e6-e2a2-46ad-ba25-caf423b73c70'
USD_WALLET_ID = '1d0e3ee6-1fac-4246-a869-9c383ae8fa9c'
BTC_WALLET_ID = '030bcff8-1bde-4b89-b814-b9c75cfda896'
VALUATION_URL = f'https://platform.the-brawl.eu/api/account/{ACCOUNT_ID}/wallet/{BTC_WALLET_ID}/valuation'

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
    "sourceWalletId": USD_WALLET_ID,
    "destWalletId": BTC_WALLET_ID,
    "amountFromSourceWallet": 10,
    "exchangeRate": 0.000023, # the lowest acceptable USD/BTC exchange rate
}, verify=False)

print(res.json())

"""
{
	'jsonapi': {
		'version': '1.0'
	},
	'data': [
		{
			'type': 'Transaction',
			'id': 'db383586-4347-4a6a-93a9-b7b8aa75a422',
			'attributes': {
				'sourceWalletId': '1d0e3ee6-1fac-4246-a869-9c383ae8fa9c',
				'amountFromSourceWallet': '10.00',
				'destWalletId': '030bcff8-1bde-4b89-b814-b9c75cfda896',
				'amountToDestWallet': '0.00022802',
				'exchangeRate': '0.000022801824328360865',
				'creatorId': '4774e5c8-4359-4a38-8205-9561187834f9',
				'state': 'done',
				'createdAt': '2023-12-09T10:00:51.587Z',
				'updatedAt': '2023-12-09T10:00:51.589Z',
				'sourceWalletVersion': '24',
				'sourceWalletBalance': '999770.00',
				'destWalletVersion': '24',
				'destWalletBalance': '0.00526128',
				'comment': None
			}
		}
	]
}
"""

res = requests.get(VALUATION_URL, headers={
    'Authorization': f'Bearer {id_token}'
}, params={
    'limit': 1,
}, verify=False)

print(res.json())

"""
[
	{
		'id': '1abd2171-6d86-4966-bf19-54408789a625',
		'balance': '0.00526128',
		'baseCurrencyBalance': '230.73943225920002',
		'createdAt': '2023-12-09T10:00:51.797Z',
		'updatedAt': '2023-12-09T10:00:51.797Z',
		'walletId': '030bcff8-1bde-4b89-b814-b9c75cfda896',
		'accountValuationId': '4502ae1d-0abf-4656-b871-2b87d56d43c8'
	}
]
"""
