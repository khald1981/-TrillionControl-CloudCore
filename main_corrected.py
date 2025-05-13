
from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "assets"
LOG_FOLDER = "logs"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

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
        ✅ التحليل المؤسسي:
        🔹 أعلى سيولة: {high}
        🔹 أدنى سيولة: {low}
        🔸 الاتجاه الأقوى: {direction}
        📈 أمر شراء: دخول = {buy_entry}, SL = {buy_sl}, TP = {buy_tp}
        📉 أمر بيع: SL = {sell_sl}, TP = {sell_tp}
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(LOG_FOLDER, f"log_{now}.txt"), "w", encoding="utf-8") as f:
            f.write(result)
        return result
    except Exception as e:
        return f"❌ خطأ أثناء المعالجة: {str(e)}"

if __name__ == "__main__":
    app.run()
