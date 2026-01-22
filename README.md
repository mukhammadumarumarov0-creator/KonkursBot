# 🎉 Konkurs Telegram Bot

Konkurs Telegram Bot is a professional Telegram bot designed to run contests, track user participation, and manage rewards. The bot integrates **user registration, referral points, Google Sheets tracking, and live broadcast announcements**.

---

## ✨ Key Features

* 🔐 **User Registration** (full name, last name, phone)
* 👥 **Group membership verification**
* 📋 **Main menu buttons:**

  * Participate in Contest
  * Gifts
  * Rules
  * My Scores
  * Admin Panel (for admins)
* 📝 **Gifts & Rules** displayed via text and images
* 🎁 **Contest Participation:**

  * Each user receives a **unique referral link**
  * Referral system: if someone joins via their link, the user earns points
* 📊 **Points Tracking:** automated and visible in admin panel & Google Sheets
* 🧑‍💼 **Admin Panel:**

  * View users and their points
  * Send messages, images, videos (normal and 360°/dunaloq)
  * Manage live broadcasts
* 🔴 **Live Broadcast (Jonli Efir):**

  * Admin enters a live link
  * Bot posts a message in the group with an inline button
  * Users who click and join can receive points

---

## 🔹 User Flow

1. User joins the **Telegram group**
2. User completes **registration** (name, surname, phone)
3. User sees **main menu buttons**
4. Reads **Gifts & Rules** (text + images)
5. Chooses **Participate in Contest** → receives a **unique referral link**
6. Referrals add points automatically
7. Admin can start **Live Broadcast (Jonli Efir)** → inline button sent to group
8. Users joining live can earn points
9. Admin tracks users & points via panel and Google Sheets

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Django** (backend & admin panel)
* **Aiogram** or **python-telegram-bot**
* **PostgreSQL / SQLite**
* **Gunicorn**
* **Nginx**
* **Google Sheets API** integration

---

## 📁 Project Structure (example)

```
KonkursBot/
├── bot/
│   ├── handlers/
│   ├── keyboards/
│   ├── states/
│   └── services/
├── contest/
│   ├── models.py
│   ├── admin.py
│   └── tests.py
├── users/
│   ├── models.py
│   └── admin.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Environment Variables (.env)

```
DEBUG=False
SECRET_KEY=your_secret_key
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=your_database_url
GOOGLE_SHEET_ID=your_sheet_id
```

---

## 👤 Registration & Verification

* Users must **join the Telegram group** first
* Registration collects **full name, surname, and phone number**
* Only registered users can access contest buttons and referral link

---

## 🎯 Contest Participation & Referral

* Each user gets a **unique referral link**
* If someone joins via that link and completes registration, the user earns **points**
* Points are tracked automatically in **admin panel and Google Sheets**

---

## 🔴 Live Broadcast (Jonli Efir)

* Admin inputs live link via panel
* Bot posts message in **group** with **inline button**
* Users click button → join live
* Bot can **automatically add points** for participation
* Admin can view live participants in **admin panel / Google Sheets**

---

## 🧑‍💼 Admin Panel

Admins can:

* View all users and points
* Send messages, images, videos (360° and normal)
* Manage contest and live broadcast
* Track user progress and referrals

---

## 📄 License

Private project, intended for contest organization and management by the owner.

---

## 👨‍💻 Author

Developed by **Muhammadumar Umarov**
Telegram: @Muhammadumar_umarov
Python Developer
