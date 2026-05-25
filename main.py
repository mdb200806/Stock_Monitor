import sys
import yfinance as yf

print("--- 株価監視プログラムを起動します ---")

# 監視リストを定義
# 買い増し用(長期)と短期トレード用を分けて管理
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

# ループで全銘柄の価格を一括取得
for ticker, name in portfolio.items():
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="2d")
        
        if len(data) >= 2:
            current = data['Close'].iloc[-1]
            prev = data['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            # 前日比がマイナスなら買い増し候補としてマーク
            alert = " [!! 注目 !!]" if change <= -2 else ""
            print(f"{name:<15} ({ticker:<8}): {current:>8.1f}円 (前日比: {change:>+6.2f}%){alert}")
        else:
            print(f"{name:<15} ({ticker:<8}): データ取得失敗")
            
    except Exception as e:
        print(f"{name} の取得中にエラーが発生しました: {e}")

print("--- チェック完了 ---")