import requests
import pandas as pd

cmc_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=1500&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap"
cmc_data = requests.get(cmc_url).json()["data"]["cryptoCurrencyList"]

cmc_df = pd.DataFrame(cmc_data)

print("Доступные столбцы:", cmc_df.columns)


# В консоли вернулось:

# Доступные столбцы: Index(['id', 'name', 'symbol', 'slug', 'cmcRank', 'marketPairCount',
#        'circulatingSupply', 'selfReportedCirculatingSupply', 'totalSupply',
#        'maxSupply', 'ath', 'atl', 'high24h', 'low24h', 'isActive',
#        'lastUpdated', 'dateAdded', 'quotes', 'isAudited', 'auditInfoList',
#        'badges'],
#       dtype='object')

# Скорее всего, объем торгов за сутки будет в "quotes" 


print(cmc_df['quotes'][0])
if "quotes" in cmc_df.columns:
    cmc_df["volume24h"] = cmc_df["quotes"].apply(lambda x: x[0]["volume24h"] if x else None)


cmc_df = cmc_df[["symbol", "name", "volume24h"]]

ss_url = "https://simpleswap.io/api/v3/currencies?fixed=false&includeDisabled=false"
ss_data = requests.get(ss_url).json()

ss_symbols = {coin["symbol"] for coin in ss_data}
print('Всего монет в simpleswap:', len(ss_symbols))

missing_coins = cmc_df[~cmc_df["symbol"].isin(ss_symbols)]

sorted_missing_coins = missing_coins.sort_values(by="volume24h", ascending=False)

print(sorted_missing_coins)