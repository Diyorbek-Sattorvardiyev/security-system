# Face Recognition Telegram Bot

Bu loyiha yuzni aniqlash va tanish uchun ishlatiladigan Telegram bot hisoblanadi. Bot kamera orqali foydalanuvchilarni aniqlaydi va natijalarni Telegram orqali yuboradi.

## 📌 Xususiyatlari
- Yuzni aniqlash va tanish
- SQLite ma'lumotlar bazasidan foydalanuvchi ma'lumotlarini yuklash
- Telegram orqali xabar, rasm va video yuborish
- LBPH yuzni tanish algoritmidan foydalanish
- OpenCV yordamida video yozish

## 🛠 Texnologiyalar
- Python
- OpenCV
- SQLite
- Telegram Bot API
- NumPy

## 📥 O'rnatish

1. Loyihani klonlash:
```sh
https://github.com/Diyorbek-Sattorvardiyev/security-system.git
  cd repository
```

2. Kerakli kutubxonalarni o'rnatish:
```sh
  pip install -r requirements.txt
```

3. `BOT_TOKEN` va `CHAT_ID` qiymatlarini `.env` fayliga qo'shing yoki kodingizda to'g'rilang.

## 📜 Foydalanish

1. Botni ishga tushirish:
```sh
  python kamera.py
```

2. Kamera orqali yuzlarni aniqlash va natijalarni Telegram bot orqali yuborish boshlanadi.

## 📷 Ishlash jarayoni
- Kamera orqali foydalanuvchi yuzini aniqlaydi.
- Agar foydalanuvchi bazada mavjud bo'lsa, uning ismi va familiyasi Telegram botga yuboriladi.
- Agar aniqlanmagan foydalanuvchi bo'lsa, noma'lum foydalanuvchi deb xabar beriladi.
- Aniqlangan jarayon videosi saqlanib, admin Telegram'iga yuboriladi.

## 📌 Muallif
- **Diyorbek** (GitHub: [your-profile](https://github.com/your-profile))

## 📝 Litsenziya
Bu loyiha ochiq manba bo‘lib, istalgancha o‘zgartirish va foydalanish mumkin.

