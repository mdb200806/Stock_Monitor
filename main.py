import yfinance as yf
import matplotlib.pyplot as plt
from googletrans import Translator

# 日本語表示の設定
plt.rcParams['font.family'] = 'MS Gothic'

# 翻訳用の関数
def translate_text(text):
    try:
        translator = Translator()
        return translator.translate(text, dest='ja').text
    except:
        return text

def get_latest_news(ticker):
    """ニュースを取得・翻訳して表示する関数"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        print(f"\n--- {ticker} の最新ニュース ---")
        if news:
            for item in news[:3]:
                # ニュースのタイトルは構造によって場所が変わるため、いくつか試す
                title = item.get('title') or item.get('content', {}).get('title') or "タイトル取得不可"
                # 発行元も探す
                provider = item.get('provider', {})
                publisher = provider.get('displayName') or item.get('publisher') or "発行元不明"
                
                print(f"- {translate_text(title)} ({publisher})")
        else:
            print("- ニュースなし")
        print("--------------------------\n")
    except Exception as e:
        print(f"ニュース取得エラー: {e}")

def show_chart(ticker, name):
    """グラフを非ブロッキング（止まらない）形式で表示する関数"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="60d")
    if not data.empty:
        data['MA25'] = data['Close'].rolling(window=25, min_periods=1).mean()
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='株価')
        plt.plot(data['MA25'], label='25日移動平均', linestyle='--')
        plt.title(f"{name} のチャート")
        plt.legend()
        plt.grid(True)
        # block=False にすることで、プログラムが止まらずに次に進む
        plt.show(block=False)
        plt.pause(0.1)

# --- 監視開始 ---
portfolio = {"8593.T": "三菱HCキャピタル", "8058.T": "三菱商事", "NVDA": "NVIDIA"}

print("--- 自動監視・解析を開始 ---")

for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    try:
        # リアルタイム価格を取得（日中対応）
        current = stock.fast_info['last_price']
        
        # 過去データでMA25を計算
        hist = stock.history(period="60d")
        ma25 = hist['Close'].rolling(window=25, min_periods=1).mean().iloc[-1]
        
        deviation = ((current - ma25) / ma25) * 100
        
        print(f"{name}: 現在 {current:.1f}円 / 乖離 {deviation:+.1f}%")
        
        if deviation <= -5:
            print("【チャンス！】")
            get_latest_news(ticker)
            show_chart(ticker, name)
            
    except Exception as e:
        print(f"{name}: データ取得でエラー発生")

print("--- チェック完了 ---")