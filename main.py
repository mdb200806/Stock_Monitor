import yfinance as yf

# 監視リスト
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

print("--- 移動平均線で買い時を判定 ---")

for ticker, name in portfolio.items():
    try:
        stock = yf.Ticker(ticker)
        # 移動平均を計算するために過去30日分のデータを取得
        data = stock.history(period="30d")
        
        if len(data) >= 25:
            current = data['Close'].iloc[-1]
            # 25日移動平均を計算
            ma25 = data['Close'].rolling(window=25).mean().iloc[-1]
            
            # 現在価格が移動平均線より5%以上安ければ「割安」と判定
            deviation = ((current - ma25) / ma25) * 100
            
            alert = " [!! 割安チャンス !!]" if deviation <= -5 else ""
            print(f"{name:<15} : 現在 {current:>8.1f}円 / 25日平均 {ma25:>8.1f}円 (乖離: {deviation:>+6.1f}%){alert}")
        
    except Exception as e:
        print(f"{name} の取得失敗")

print("--- チェック完了 ---")