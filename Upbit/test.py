import requests
import json
import threading
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
# get exchanges krw
# https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD,FRX.KRWJPY,FRX.KRWCNY,FRX.KRWEUR
def get_usd_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange =requests.get(url, headers=headers).json()
    return exchange[0]['cashBuyingPrice']
#     return exchange[0]['basePrice']

# https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-BTC
def get_last_price(coin_name):
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-{coin_name}'.format(coin_name=coin_name)
    tickValue =  requests.get(url, headers=headers).json()
    return tickValue[0]['tradePrice']

def get_ticker(coin_name):
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

lastPriceBTC = 8387000 # 2018-02-07
lastPriceADA = 371 # 2018-02-07
lastPriceNEO = 113100 # 2018-02-07
lastPricePOWR = 715 # 2018-02-07

def on_timer():
    bitfinexBTCUSD = get_ticker('tBTCUSD')
    LastBTCUSD = bitfinexBTCUSD['LAST_PRICE']
    USDKRW = get_usd_krw() # from KEB Bank
    changedBTCKRW = LastBTCUSD * USDKRW
    
    upbitBTCKRW = get_last_price('BTC')
    upbitADAKRW = get_last_price('ADA')
    upbitNEOKRW = get_last_price('NEO')
    upbitPOWRKRW = get_last_price('POWR')
    
    ratio_btc = ((upbitBTCKRW-lastPriceBTC)/lastPriceBTC)*100
    ratio_ada = ((upbitADAKRW-lastPriceADA)/lastPriceADA)*100
    ratio_neo = ((upbitNEOKRW-lastPriceNEO)/lastPriceNEO)*100
    ratio_powr = ((upbitPOWRKRW-lastPricePOWR)/lastPricePOWR)*100
    
    # calculate premium
    diff = upbitBTCKRW - changedBTCKRW
    preminum = (diff / changedBTCKRW) * 100
    
    print("----------------------")
    print("%12s = %.2f"%('upbit(KRW)', upbitBTCKRW))
    print("%12s = %.2f"%('bitfi(KRW)', changedBTCKRW))
    print("%12s = %d"%('Diff (KRW)', int(diff)))
    print("%12s = %.2f %%"%('Preminum', preminum))
    print("%12s = %d(%.2f %%)"%('BTC(KRW)', upbitBTCKRW, ratio_btc))
    print("%12s = %d(%.2f %%)"%('ADA(KRW)', upbitADAKRW, ratio_ada))
    print("%12s = %d(%.2f %%)"%('NEO(KRW)', upbitNEOKRW, ratio_neo))
    print("%12s = %d(%.2f %%)"%('POWR(KRW)', upbitPOWRKRW, ratio_powr))
    print("----------------------")
    timer = threading.Timer(30, on_timer)
    timer.start()

def stop_timer():
    timer.cancel()

timer = threading.Timer(1, on_timer)
timer.start()

