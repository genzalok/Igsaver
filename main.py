import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, FORCE_SUB_CHANNEL, DUMP_CHANNEL_ID
from utils import check_user_membership, download_instagram_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member_ok = await check_user_membership(context.bot, user.id, FORCE_SUB_CHANNEL)
    if not member_ok:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}")]]
        await update.message.reply_text("Please join the channel to use this bot.", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    await update.message.reply_text("Send me an Instagram link (post/reel/video).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user = update.effective_user

    member_ok = await check_user_membership(context.bot, user.id, FORCE_SUB_CHANNEL)
    if not member_ok:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}")]]
        await update.message.reply_text("Please join the channel to use this bot.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await context.bot.send_message(DUMP_CHANNEL_ID, f"User: {user.username or user.id}
Sent: {url}")

    video_url = download_instagram_video(url)
    if video_url:
        await update.message.reply_video(video_url)
    else:
        await update.message.reply_text("Failed to fetch video. Make sure the link is public.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
