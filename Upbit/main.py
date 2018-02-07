import bitfinex
import upbit
import threading

bitfinexBTCUSD = bitfinex.get_ticker('tBTCUSD')
LastBTCUSD = bitfinexBTCUSD['LAST_PRICE']
USDKRW = upbit.get_usd_krw() # from KEB Bank
changedBTCKRW = LastBTCUSD * USDKRW
upbitBTCKRW = upbit.get_last_price('BTC')

print('upbit(KRW) = ', upbitBTCKRW)
print('bitfi(KRW) = ', changedBTCKRW)
print('bitfi(USD) = ', LastBTCUSD)

# calculate premium
diff = upbitBTCKRW - changedBTCKRW
preminum = (diff / changedBTCKRW) * 100
print('diff(KRW) = ', int(diff))
print('preminum = %.02f'% preminum)