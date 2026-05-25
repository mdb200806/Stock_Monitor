import yfinance as yf
import matplotlib.pyplot as plt

# 日本語フォント設定
plt.rcParams['font.family'] = 'MS Gothic'

def get_latest_news(ticker):
    """ニュースを取得する関数"""
    stock = yf.Ticker(ticker)
    news = stock.news
    print(f"\n--- {ticker} の最新ニュース ---")
    for item in news[:3]:
        print(f"- {item['title']} ({item['publisher']})")
    print("--------------------------\n")

def show_chart(ticker, name):
    """グラフを表示する関数"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="90d")
    data['MA25'] = data['Close'].rolling(window=25).mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='株価', color='blue')
    plt.plot(data['MA25'], label='25日移動平均', color='red', linestyle='--')
    plt.title(f"{name} ({ticker}) - チャートを確認してください！")
    plt.legend()
    plt.grid(True)
    plt.show()

# 監視リスト
portfolio = {"8593.T": "三菱HCキャピタル", "8058.T": "三菱商事", "NVDA": "NVIDIA"}

print("--- 自動監視・解析を開始 ---")
for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    data = stock.history(period="30d")
    
    if len(data) >= 25:
        current = data['Close'].iloc[-1]
        ma25 = data['Close'].rolling(window=25).mean().iloc[-1]
        deviation = ((current - ma25) / ma25) * 100
        
        if deviation <= -5:
            print(f"【チャンス！】{name}が割安です！({deviation:.1f}%)")
            get_latest_news(ticker) # ニュース追加
            show_chart(ticker, name) # グラフ表示
        else:
            print(f"{name}: 乖離率 {deviation:+.1f}% (監視中)")