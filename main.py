import yfinance as yf
import matplotlib.pyplot as plt

def show_chart(ticker, name):
    """銘柄を受け取ってグラフを表示する関数"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="90d") # 少し長めの90日分
    data['MA25'] = data['Close'].rolling(window=25).mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Price', color='blue')
    plt.plot(data['MA25'], label='MA25', color='red', linestyle='--')
    plt.title(f"{name} ({ticker}) - Check this chart!")
    plt.legend()
    plt.grid(True)
    plt.show()

# 監視リスト
portfolio = {"8593.T": "三菱HCキャピタル", "8058.T": "三菱商事", "NVDA": "NVIDIA"}

print("--- 自動監視・解析を開始 ---")
for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    data = stock.history(period="30d")
    current = data['Close'].iloc[-1]
    ma25 = data['Close'].rolling(window=25).mean().iloc[-1]
    deviation = ((current - ma25) / ma25) * 100
    
    # 判定：もし乖離率が-5%以下ならグラフを表示！
    if deviation <= -5:
        print(f"【チャンス！】{name}が割安です！({deviation:.1f}%) -> グラフを表示します")
        show_chart(ticker, name)
    else:
        print(f"{name}: 乖離率 {deviation:+.1f}% (監視中)")