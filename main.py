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
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    filename = request.form.get("filename")
    filepath = os.path.join(DATA_FOLDER, filename)
    try:
        df = pd.read_csv(filepath)
        high = df['High'].max()
        low = df['Low'].min()
        last_close = df['Close'].iloc[-1]
        last_open = df['Open'].iloc[-1]
        direction = "🔼 الشراء أقوى" if last_close > last_open else "🔽 البيع أقوى"
        entry = last_close
        sl_buy = entry - 2
        tp_buy = entry + 4
        sl_sell = entry + 2
        tp_sell = entry - 4
        log = f"""
التحليل لملف: {filename}
🔍 أعلى سيولة: {high}
🔍 أدنى سيولة: {low}
🤖 اتجاه السوق: {direction}
📌 أمر شراء: دخول = {entry}, وقف = {sl_buy}, هدف = {tp_buy}
📌 أمر بيع: دخول = {entry}, وقف = {sl_sell}, هدف = {tp_sell}
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(os.path.join(LOG_FOLDER, f"log_{timestamp}.txt"), "w") as f:
            f.write(log)
        return log.replace("\n", "<br>")
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)