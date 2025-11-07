import json
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = "8390594731:AAG8jQPegBJGGL67XqQuvZcAR-_bC3KtHEc"

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN not found! Please check your .env file.")

# JSON helpers
def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

LESSONS = load_json("data/lessons.json")
USERS_FILE = "data/users.json"

# ---------------- COMMANDS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_firstname = update.effective_user.first_name

    users_data = load_json(USERS_FILE)
    if not any(u["id"] == user_id for u in users_data["users"]):
        users_data["users"].append({"id": user_id, "progress": {}})
        save_json(USERS_FILE, users_data)

    keyboard = [
        [InlineKeyboardButton("📚 View Courses", callback_data="view_courses")],
        [InlineKeyboardButton("📊 My Progress", callback_data="progress")]
    ]
    await update.message.reply_text(
        f"Welcome {user_firstname}! 👋\n\nChoose what you want to do:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- HANDLERS ---------------- #

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    users_data = load_json(USERS_FILE)
    user = next((u for u in users_data["users"] if u["id"] == user_id), None)
    await query.answer()
    data = query.data

    if data == "view_courses":
        buttons = []
        for module in LESSONS["modules"]:
            progress = user["progress"].get(str(module["id"]), {})
            status = "✅" if progress.get("completed") else "⬜"
            buttons.append([InlineKeyboardButton(f"{status} {module['title']}", callback_data=f"course_{module['id']}")])
        await query.message.reply_text("📘 *Available Courses:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("course_"):
        module_id = int(data.split("_")[1])
        module = next((m for m in LESSONS["modules"] if m["id"] == module_id), None)
        if not module:
            await query.message.reply_text("⚠️ Course not found.")
            return

        # Lock next courses
        if module_id > 1:
            prev = user["progress"].get(str(module_id - 1), {})
            if not prev.get("completed"):
                await query.message.reply_text("🚫 You must complete the previous course before accessing this one.")
                return

        text = f"📘 *{module['title']}*\n\n{module.get('description', '')}\n\n🔗 [Open Course PDF]({module['pdf']})"
        buttons = [[InlineKeyboardButton("🧩 Take Quiz", callback_data=f"quiz_{module_id}")]]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("quiz_"):
        module_id = int(data.split("_")[1])
        module = next((m for m in LESSONS["modules"] if m["id"] == module_id), None)
        quiz_pool = module["quiz"]
        selected = random.sample(quiz_pool, min(5, len(quiz_pool)))
        context.user_data["quiz"] = selected
        context.user_data["score"] = 0
        context.user_data["index"] = 0
        await send_question(update, context, module_id)

    elif data.startswith("answer_"):
        _, module_id, q_index, chosen = data.split("_")
        module_id, q_index, chosen = int(module_id), int(q_index), int(chosen)
        quiz = context.user_data["quiz"]
        question = quiz[q_index]
        correct = question["answer"]

        if chosen == correct:
            context.user_data["score"] += 1

        next_q = q_index + 1
        if next_q < len(quiz):
            context.user_data["index"] = next_q
            await send_question(update, context, module_id)
        else:
            score = context.user_data["score"]
            percentage = int((score / len(quiz)) * 100)
            users_data = load_json(USERS_FILE)
            user = next((u for u in users_data["users"] if u["id"] == update.effective_user.id), None)
            user["progress"][str(module_id)] = {"score": percentage, "completed": percentage >= 50}
            save_json(USERS_FILE, users_data)

            result_msg = "✅ Passed!" if percentage >= 50 else "❌ Failed!"
            await query.message.reply_text(f"🎯 Your score: {percentage}%\n{result_msg}")

    elif data == "progress":
        progress = user["progress"]
        if not progress:
            await query.message.reply_text("You haven’t completed any modules yet.")
            return
        result = "\n".join([f"📘 {LESSONS['modules'][int(mid)-1]['title']}: {info['score']}% {'✅' if info['completed'] else '❌'}" for mid, info in progress.items()])
        await query.message.reply_text(f"📊 *Your Progress:*\n{result}", parse_mode="Markdown")

async def send_question(update, context, module_id):
    query = update.callback_query
    q_index = context.user_data["index"]
    question = context.user_data["quiz"][q_index]
    buttons = [[InlineKeyboardButton(opt, callback_data=f"answer_{module_id}_{q_index}_{i}")] for i, opt in enumerate(question["options"])]
    await query.message.reply_text(f"Q{q_index+1}: {question['question']}", reply_markup=InlineKeyboardMarkup(buttons))

# ---------------- MAIN ---------------- #

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("✅ Bot running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    print("🚀 Starting bot...")
    main()