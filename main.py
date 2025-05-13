from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "assets"
LOG_FOLDER = "logs"
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get("datafile")
    if not file:
        return "❌ لم يتم رفع أي ملف."
    
    try:
        df = pd.read_csv(file)
        high = df['High'].max()
        low = df['Low'].min()
        last_close = df['Close'].iloc[-1]
        last_open = df['Open'].iloc[-1]
        direction = "🔼 الشراء أقوى" if last_close > last_open else "🔽 البيع أقوى"
        
        buy_entry = last_close
        buy_sl = buy_entry - 2
        buy_tp = buy_entry + 4

        sell_sl = buy_entry + 2
        sell_tp = buy_entry - 4

        result = f"""
        🔍 أعلى سيولة: {high}<br>
        🔍 أدنى سيولة: {low}<br>
        🤖 اتجاه السوق: {direction}<br>
        📌 أمر شراء: دخول = {buy_entry}, وقف = {buy_sl}, هدف = {buy_tp}<br>
        📌 أمر بيع: دخول = {buy_entry}, وقف = {sell_sl}, هدف = {sell_tp}<br>
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(os.path.join(LOG_FOLDER, f"session_{timestamp}.log"), 'w', encoding='utf-8') as f:
            f.write(result.replace("<br>", "\n"))

        return result
    except Exception as e:
        return f"❌ خطأ في التحليل: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)