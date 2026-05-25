import yfinance as yf
import matplotlib.pyplot as plt
from googletrans import Translator

# 日本語フォント設定
plt.rcParams['font.family'] = 'MS Gothic'

# 翻訳関数
def translate_text(text):
    try:
        translator = Translator()
        return translator.translate(text, dest='ja').text
    except:
        return text

def get_latest_news(ticker):
    try:
        stock = yf.Ticker(ticker)
        # ニュースデータをもっと詳細に取得
        news = stock.news
        print(f"\n--- {ticker} の最新ニュース ---")
        
        if not news:
            print("- ニュースは見つかりませんでした。")
            return

        for item in news[:3]:
            # タイトル取得の探索範囲を広げる
            title = item.get('title') or item.get('content', {}).get('title', 'タイトル取得不可')
            publisher = item.get('publisher', '発行元不明')
            
            # 翻訳を試みる（エラーなら英語タイトルをそのまま出す）
            print(f"- {translate_text(title)} ({publisher})")
            
        print("--------------------------\n")
    except Exception as e:
        print(f"ニュース取得中にエラー発生: {e}")

def show_chart(ticker, name):
    stock = yf.Ticker(ticker)
    data = stock.history(period="60d")
    data['MA25'] = data['Close'].rolling(window=25, min_periods=1).mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='株価')
    plt.plot(data['MA25'], label='25日移動平均', linestyle='--')
    plt.title(f"{name} のチャート")
    plt.legend()
    plt.grid(True)
    plt.show()

portfolio = {"8593.T": "三菱HCキャピタル", "8058.T": "三菱商事", "NVDA": "NVIDIA"}

print("--- 自動監視・解析を開始 ---")

for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    try:
        current = stock.fast_info['last_price']
        hist = stock.history(period="60d")
        ma25 = hist['Close'].rolling(window=25, min_periods=1).mean().iloc[-1]
        deviation = ((current - ma25) / ma25) * 100
        
        print(f"{name}: 現在 {current:.1f}円 / 乖離 {deviation:+.1f}%")
        
        if deviation <= -5:
            print("【チャンス！】")
            get_latest_news(ticker)
            show_chart(ticker, name)
    except Exception as e:
        print(f"{name}: データ取得でエラー発生 {e}")

print("--- チェック完了 ---")