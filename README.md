# Drmnef EFI Generator

أداة تلقائية لإنشاء ملف EFI خاص بالهاكنتوش باستخدام Python.

## المميزات

- استخراج مواصفات الجهاز وحفظها.
- تحميل أحدث إصدار من OpenCore.
- إنشاء مجلد EFI تلقائيًا.
- تحميل الكيستات الأساسية (Lilu, VirtualSMC, AppleALC, WhateverGreen).
- تحميل وتحويل ملفات SSDT (مثل SSDT-EC, SSDT-AWAC, وغيرها).
- دعم كامل لأنظمة Windows و Linux.
- تأثيرات مرئية متحركة (Animated UI).

## المتطلبات

- Python 3.8 أو أحدث.
- اتصال إنترنت.

## طريقة التشغيل

```bash
python Drmnef-EFI.py
```

في حال عدم وجود المكتبات، سيتم تثبيتها تلقائيًا.

## المطور

- منيف المضياني (Drmnef)
- 📧 Dr.mnef@gmail.com
![عرض مرئي لعمل السكربت](Drmnef-efi.gif)
