from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os

# === Mapping Logic ===
def get_colors(num):
    if num == 0:
        return ['red', 'violet']
    elif num == 5:
        return ['green', 'violet']
    elif num in [2, 4, 6, 8]:
        return ['red']
    elif num in [1, 3, 7, 9]:
        return ['green']
    else:
        return []

def dominant_color(color_list):
    if 'red' in color_list:
        return 'red'
    elif 'green' in color_list:
        return 'green'
    else:
        return 'violet'

# === Bot Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send /predict followed by last 3 numbers.\nExample:\n/predict 2 0 5")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nums = list(map(int, context.args))
        if len(nums) < 3:
            await update.message.reply_text("❌ Enter at least 3 numbers. Example:\n/predict 2 0 5")
            return

        last_colors = [dominant_color(get_colors(n)) for n in nums[-3:]]
        last = last_colors[-1]
        streak = 1
        for i in range(2, 0, -1):
            if last_colors[i] == last_colors[i-1]:
                streak += 1
            else:
                break

        if last == 'red':
            prediction = 'green' if streak >= 4 else 'red'
        elif last == 'green':
            prediction = 'red' if streak >= 3 else 'green'
        else:
            prediction = 'red'

        violet_trigger = 'yes' if nums[-1] in [0, 5] else 'no'

        await update.message.reply_text(
            f"📊 Last colors: {', '.join(last_colors)}\n"
            f"🔮 Predicted main color: *{prediction.upper()}*\n"
            f"🎭 Violet chance: *{violet_trigger.upper()}*",
            parse_mode='Markdown'
        )
    except:
        await update.message.reply_text("⚠️ Invalid format. Use: /predict 2 0 5")

# === Start the bot ===
def run():
    TOKEN = os.environ.get("BOT_TOKEN")
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()

if __name__ == "__main__":
    run()
