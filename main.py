import yfinance as yf
import matplotlib.pyplot as plt
from googletrans import Translator
import threading

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
                # 取得経路を複数試してタイトルを確実に拾う
                title = item.get('title') or item.get('content', {}).get('title') or "タイトル取得不可"
                provider = item.get('provider', {})
                publisher = provider.get('displayName') or item.get('publisher') or "発行元不明"
                print(f"- {translate_text(title)} ({publisher})")
        else:
            print("- ニュースなし")
        print("--------------------------\n")
    except Exception:
        print("ニュース取得エラー")

def show_chart(ticker, name):
    """グラフを別スレッドで起動してメインプログラムを止めない関数"""
    def _plot():
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
            plt.show()

    # 別スレッドで実行開始
    thread = threading.Thread(target=_plot)
    thread.start()

# --- 監視開始 ---
portfolio = {
    # 長期・買い増し枠
    "8593.T": "三菱HCキャピタル",
    "8058.T": "三菱商事",
    "4502.T": "武田薬品工業",
    "4503.T": "アステラス製薬",
    "8306.T": "三菱UFJ",
    "2914.T": "JT",
    
    # 短期トレード用（半導体・AIインフラ）
    "SOXX": "半導体ETF",
    "FANG": "FANG+ ETF",
    "NVDA": "NVIDIA",
    "2244.T": "米国半導体ETF"
}

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
        
        # 乖離が-5%以下ならチャンスと判断
        if deviation <= -5:
            print("【チャンス！】")
            get_latest_news(ticker)
            show_chart(ticker, name)
            
    except Exception:
        print(f"{name}: データ取得でエラー発生")

print("--- チェック完了 ---")