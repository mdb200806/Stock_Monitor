import yfinance as yf
import matplotlib.pyplot as plt

# 日本語フォント設定
plt.rcParams['font.family'] = 'MS Gothic'

def get_latest_news(ticker):
    """ニュース取得関数"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        print(f"\n--- {ticker} の最新ニュース ---")
        if news:
            for item in news[:3]:
                content = item.get('content', {})
                title = content.get('title', 'タイトルなし')
                publisher = item.get('provider', {}).get('displayName', '発行元不明')
                print(f"- {title} ({publisher})")
        else:
            print("- ニュースなし")
        print("--------------------------\n")
    except Exception:
        print("ニュース取得失敗")

def show_chart(ticker, name):
    """チャート表示関数"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="60d")
    
    # 過去データから移動平均を計算
    data['MA25'] = data['Close'].rolling(window=25, min_periods=1).mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='過去株価(終値)')
    plt.plot(data['MA25'], label='25日移動平均', linestyle='--')
    plt.title(f"{name} ({ticker})")
    plt.legend()
    plt.grid(True)
    plt.show()

# 監視リスト
portfolio = {"8593.T": "三菱HCキャピタル", "8058.T": "三菱商事", "NVDA": "NVIDIA"}

print("--- 自動監視・解析を開始 ---")

for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    
    # 1. リアルタイム価格を取得（終値確定を待たずに現在値を取得）
    try:
        current = stock.fast_info['last_price']
    except:
        print(f"{name}: 現在価格取得失敗")
        continue

    # 2. 過去60日分の終値を取得して移動平均を算出
    hist = stock.history(period="60d")
    if hist.empty:
        print(f"{name}: 過去データ取得失敗")
        continue
        
    ma25 = hist['Close'].rolling(window=25, min_periods=1).mean().iloc[-1]
    
    # 3. 乖離率を計算
    deviation = ((current - ma25) / ma25) * 100
    
    print(f"{name}: 現在 {current:.1f}円 / 平均 {ma25:.1f}円 (乖離: {deviation:+.1f}%)")
    
    # 4. 判定
    if deviation <= -5:
        print(f"【チャンス！】{name}が割安です！")
        get_latest_news(ticker)
        show_chart(ticker, name)

print("--- チェック完了 ---")