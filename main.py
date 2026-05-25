import yfinance as yf
import matplotlib.pyplot as plt
from googletrans import Translator
import queue

# 日本語表示の設定
plt.rcParams['font.family'] = 'MS Gothic'

# 翻訳用の関数
def translate_text(text):
    try:
        translator = Translator()
        return translator.translate(text, dest='ja').text
    except:
        return text

# ニュース取得関数
def get_latest_news(ticker):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        print(f"\n--- {ticker} の最新ニュース ---")
        if news:
            for item in news[:3]:
                title = item.get('title') or item.get('content', {}).get('title') or "タイトル取得不可"
                publisher = item.get('provider', {}).get('displayName') or item.get('publisher') or "発行元不明"
                print(f"- {translate_text(title)} ({publisher})")
        else:
            print("- ニュースなし")
        print("--------------------------\n")
    except Exception:
        print("ニュース取得エラー")

# 監視リスト（あなたの設定をそのまま反映）
portfolio = {
    "8593.T": "三菱HCキャピタル",
    "8058.T": "三菱商事",
    "4502.T": "武田薬品工業",
    "4503.T": "アステラス製薬",
    "8306.T": "三菱UFJ",
    "2914.T": "JT",
    "SOXX": "半導体ETF",
    "FANG": "FANG+ ETF",
    "NVDA": "NVIDIA",
    "2244.T": "米国半導体ETF"
}

# グラフ待ち行列
chart_queue = queue.Queue()

print("--- 自動監視・解析を開始 ---")

for ticker, name in portfolio.items():
    stock = yf.Ticker(ticker)
    try:
        current = stock.fast_info['last_price']
        hist = stock.history(period="60d")
        if hist.empty: continue
        
        ma25 = hist['Close'].rolling(window=25, min_periods=1).mean().iloc[-1]
        deviation = ((current - ma25) / ma25) * 100
        
        print(f"[{name}] 現在: {current:.1f} / 乖離: {deviation:+.1f}%")
        
        if deviation <= -5:
            print(f"  >>> 【チャンス！】割安です！")
            get_latest_news(ticker)
            chart_queue.put((ticker, name))
            
    except Exception:
        print(f"[{name}]: データ取得エラー")

# 最後に、溜まったグラフをメインスレッドで表示
if not chart_queue.empty():
    print("\n--- 全計算完了！グラフ描画を開始します ---")
    while not chart_queue.empty():
        ticker, name = chart_queue.get()
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

print("\n--- 全ての処理が完了しました ---")