# TrillionControl – ΣΩ | CloudCore

📡 سحابة التحكم السيادي الكامل لتحليل الأسواق وتشغيل الأوامر الذكية

## مميزات
- تحليل مؤسسي للأصول من ملفات CSV
- توليد أوامر شراء وبيع تلقائيًا
- مقارنة اتجاهات السوق
- حفظ الجلسات وتحليل السيولة
- واجهة Web باستخدام Flask
- قابل للنشر على Render.com

## ملفات رئيسية
- `main.py`: الخادم الرئيسي
- `templates/index.html`: الواجهة
- `requirements.txt`: التبعيات
- `Procfile`: أمر التشغيل في Render

## للتشغيل المحلي:
```bash
pip install -r requirements.txt
python main.py
```

## التحليل السحابي:
يتم التشغيل تلقائيًا على Render مع مجلد `assets` لتحميل البيانات و `logs` لتخزين التحليلات.

ΣΩ — Sovereignty Engine.