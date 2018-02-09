import requests
import json
import threading
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# https://crix-api-endpoint.upbit.com/v1/crix/trades/days?code=CRIX.UPBIT.KRW-BTC&count=2
def upbit_get_last_trades(name):

    url = "https://crix-api-endpoint.upbit.com/v1/crix/trades/days?code=CRIX.UPBIT.KRW-{CoinName}&count=1".format(CoinName=name)
    trades = requests.get(url, headers=headers).json()
    return trades[0]

# get exchanges krw
# https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD,FRX.KRWJPY,FRX.KRWCNY,FRX.KRWEUR
def upbit_get_usd_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange =requests.get(url, headers=headers).json()
#     return exchange[0]['cashBuyingPrice']
    return exchange[0]['tcBuyingPrice']

# https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-BTC
def get_last_price(coin_name):
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-{coin_name}'.format(coin_name=coin_name)
    tickValue =  requests.get(url, headers=headers).json()
    return tickValue[0]['tradePrice']

def bitfinex_get_ticker(coin_name):
    url = "https://api.bitfinex.com/v2/ticker/{coin}".format(coin=coin_name)
    info = requests.get(url, headers=headers).json() # [BID ,BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
    # BID    float    Price of last highest bid
    # BID_SIZE    float    Size of the last highest bid
    # ASK    float    Price of last lowest ask
    # ASK_SIZE    float    Size of the last lowest ask
    # DAILY_CHANGE    float    Amount that the last price has changed since yesterday
    # DAILY_CHANGE_PERC    float    Amount that the price has changed expressed in percentage terms
    # LAST_PRICE    float    Price of the last trade
    # VOLUME    float    Daily volume
    # HIGH    float    Daily high
    # LOW    float    Daily low
    dict_info = {}
    keys = [ 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_PERC', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW']
    idx = 0
    for key in keys:
        dict_info[key] = info[idx]
        idx = idx + 1
    return dict_info

def on_timer():
    # get upbit price
    upbit_trade_BTCKRW = upbit_get_last_trades("BTC")
    upbit_trade_ADAKRW = upbit_get_last_trades("ADA")
    upbit_trade_XRPKRW = upbit_get_last_trades("XRP")
    upbit_trade_NEOKRW = upbit_get_last_trades("NEO")
    # get bitfinex price
    bitfinexBTCUSD = bitfinex_get_ticker('tBTCUSD')
    
    upbit_prevClosing_BTCKRW =   upbit_trade_BTCKRW["prevClosingPrice"]
    upbit_tradePrice_BTCKRW = upbit_trade_BTCKRW["tradePrice"]
    upbit_chg_ratio_BTCKRW = ((upbit_tradePrice_BTCKRW-upbit_prevClosing_BTCKRW)/upbit_prevClosing_BTCKRW) * 100
    
    upbit_prevClosing_ADAKRW =   upbit_trade_ADAKRW["prevClosingPrice"]
    upbit_tradePrice_ADAKRW = upbit_trade_ADAKRW["tradePrice"]
    upbit_chg_ratio_ADAKRW = ((upbit_tradePrice_ADAKRW-upbit_prevClosing_ADAKRW)/upbit_prevClosing_ADAKRW) * 100
    
    upbit_prevClosing_XRPKRW =   upbit_trade_XRPKRW["prevClosingPrice"]
    upbit_tradePrice_XRPKRW = upbit_trade_XRPKRW["tradePrice"]
    upbit_chg_ratio_XRPKRW = ((upbit_tradePrice_XRPKRW-upbit_prevClosing_XRPKRW)/upbit_prevClosing_XRPKRW) * 100
    
    upbit_prevClosing_NEOKRW =   upbit_trade_NEOKRW["prevClosingPrice"]
    upbit_tradePrice_NEOKRW = upbit_trade_NEOKRW["tradePrice"]
    upbit_chg_ratio_NEOKRW = ((upbit_tradePrice_NEOKRW-upbit_prevClosing_NEOKRW)/upbit_prevClosing_NEOKRW) * 100
  
    
    LastBTCUSD = bitfinexBTCUSD['LAST_PRICE']
    USDKRW = upbit_get_usd_krw() # from KEB Bank
    bitfinex_BTCKRW = LastBTCUSD * USDKRW
   

    # calculate premium
    diff = upbit_tradePrice_BTCKRW - bitfinex_BTCKRW
    preminum = (diff / bitfinex_BTCKRW) * 100
    

    print("----------------------")
    print("%12s = %s"%('bitfi(USD)', format(LastBTCUSD, ",.2f")))
    print("%12s = %s"%('Diff(KRW)', format(diff, ",.2f")))
    print("%12s = %.2f %%"%('Preminum', preminum))
    print("%12s = %s(%.2f %%)"%('BTC(KRW)', format(upbit_tradePrice_BTCKRW, ",.1f"), upbit_chg_ratio_BTCKRW))
    print("%12s = %s(%.2f %%)"%('ADA(KRW)', format( int(upbit_tradePrice_ADAKRW), ",d"), upbit_chg_ratio_ADAKRW))
    print("%12s = %s(%.2f %%)"%('XRP(KRW)', format( int(upbit_tradePrice_XRPKRW), ",d"), upbit_chg_ratio_XRPKRW))
    print("%12s = %s(%.2f %%)"%('NEO(KRW)', format( int(upbit_tradePrice_NEOKRW), ",d"), upbit_chg_ratio_NEOKRW))
    print("----------------------")
    
on_timer()
#     timer = threading.Timer(30, on_timer)
#     timer.start()

# timer = threading.Timer(1, on_timer)
# timer.start()

