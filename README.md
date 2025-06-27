# Drmnef EFI Generator

أداة تلقائية لإنشاء ملف EFI خاص بالهاكنتوش باستخدام Python.

## المميزات

- استخراج مواصفات الجهاز وحفظها.
- تحميل أحدث إصدار من OpenCore.
- إنشاء مجلد EFI تلقائيًا.
- تحميل الكيستات الأساسية (Lilu, VirtualSMC, AppleALC, WhateverGreen).
- تحميل وتحويل ملفات SSDT (مثل SSDT-EC, SSDT-AWAC, وغيرها).
- دعم كامل لأنظمة Windows و Linux.


## المتطلبات

- Python 3.8 أو أحدث.
- اتصال إنترنت.

## طريقة التشغيل

```bash
python Drmnef-EFI.py
```
التثبيت على كالي لينكس
![عرض مرئي لعمل السكربت](Drmnef-efi.gif)

التثبيت في الويندوز 
![عرض مرئي لعمل السكربت](Drmnef-efii.gif)

في حال عدم وجود المكتبات، سيتم تثبيتها تلقائيًا.

## المطور

- منيف المضياني (Drmnef)
- 📧 Dr.mnef@gmail.com

