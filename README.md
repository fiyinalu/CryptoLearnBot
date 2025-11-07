🤖 CryptoLearnBot

CryptoLearnBot is a Telegram-based educational bot designed to teach users about Decentralized Finance (DeFi) through bite-sized lessons, interactive quizzes, and progress tracking.

It is perfect for beginners who want to understand crypto and DeFi in a fun, structured way.

---

🌟 Features

📘 **Modular Learning System** — Learn DeFi through structured modules.
📄 **Resource Access** — Each module includes a PDF resource link.
🧠 **Quizzes** — 5–15 multiple-choice questions after each lesson.
🔒 **Progress Lock** — Users must score at least **50%** to unlock the next module.
✅ **Progress Tracker** — Displays completed modules with green checkmarks.
💬 **Easy Commands** — Simple Telegram commands for navigation.

---

## Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/CryptoLearnBot.git
cd CryptoLearnBot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # (macOS/Linux)
venv\Scripts\activate         # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

In the root directory, create a file named `.env` and add:

```
BOT_TOKEN=your_telegram_bot_token_here
```

### 5️⃣ Run the Bot

```bash
python -m src.bot
```

---

## 🧩 Project Structure

```
CryptoLearnBot/
│
├── data/
│   ├── lessons.json        # Course and quiz data
│   └── users.json          # User progress data
│
├── src/
│   └── bot.py              # Main bot logic
│
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 💡 How It Works

1. When a user types `/start`, the bot greets them and offers to start learning.
2. The user selects “Start Learning” to view available modules.
3. Each module provides a link to its DeFi learning material (hosted on Google Drive).
4. After studying, the user answers a 5-question quiz.
5. A score of **50% or more** unlocks the next module automatically.
6. Progress is stored in `data/users.json`.

---

## 🧰 Built With

* [Python Telegram Bot](https://docs.python-telegram-bot.org/)
* [dotenv](https://pypi.org/project/python-dotenv/)
* JSON for data storage

---

## 📈 Future Enhancements

* Upload PDFs directly to the bot
* Add image and video lessons
* Track quiz scores and display badges
* Add community leaderboard

---

## 🪙 License

This project is licensed under the **MIT License** — free to use, modify, and build on.
