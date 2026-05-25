import sys

print("環境設定が完了しました！")
print("現在のPythonの場所:", sys.executable)

import yfinance as yf

# 三菱HCキャピタル（8593.T）の株価を取得
ticker = "8593.T"
stock = yf.Ticker(ticker)
price = stock.history(period="1d")['Close'].iloc[-1]

print(f"{ticker} の現在価格: {price:.1f}円")

#test
print