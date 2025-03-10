import logging
import re
import random
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('🐒')

# Define the message handler to delete links or respond to specific ones
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    text = message.text
    user = message.from_user
    user_name = user.first_name
    user_username = user.username
    user_link = f"{user_name} (@{user_username})" if user_username else user_name

    # Updated regex pattern to match both https://t.me/nft/ and t.me/nft/
    nft_pattern = r"(https://t.me/nft/|t.me/nft/)(\w+)-(\d+)"
    match = re.search(nft_pattern, text)

    if match:
        gift_name = match.group(2)
        gift_number = match.group(3)
        response_text = (
            f"🐵 *Пользователь {user_link} отправляет ссылку на коллекционный подарок!*\n\n"
            f"🔗 *Отправленная ссылка:* {text}\n\n"
            f"🎁 *Название подарка:* `{gift_name}`\n"
            f"🔢 *Номер подарка:* `{gift_number}`"
        )
        await message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)
        await message.delete()
    elif 'http://' in text or 'https://' in text or 't.me/' in text:
        await message.delete()

    context.chat_data['message_count'] = context.chat_data.get('message_count', 0) + 1
    if context.chat_data['message_count'] >= 10:
        context.chat_data['message_count'] = 0
        await send_random_message(context)

async def send_random_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = -1002357945884
    messages = [
        "когда новые подарки?",
        "блин когда уже нфт новые выпустят",
        "че у вас тут происходит",
        "дарова шпана",
        "астеро легенда, че еще сказать",
        "салам алейкум",
        "хелоу чатек",
        "админы на месте, всем спать",
        "ну что вы, макаки, не спите еще? 🙊",
        "когда нови подарунки 🎁🐒",
        "я @ ты @ я @ ты @",
        "але админы",
        "чат умер чето",
        "все понял, ливаю отсюда",
        "блин, случайно из группы с подарками вышел, киньте кто то ее снова",
        "сижу короче, слежу за минтами в @GiftsMinterBot, кто тоже ставьте +",
        "кто будет моей девушкой ставьте +, посмотрим сколько нас",
        "дарова всем кого не видел",
        "ебать че тут происходит у вас",
        "ахахахах пиздец",
        "авхахха",
        "АХХПАХВХАХВХ"
    ]
    random_message = random.choice(messages)
    await context.bot.send_message(chat_id=chat_id, text=random_message)

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token("7998421928:AAGs7WUfu-2lRzAOY7H8aU-iesEK7RB63B0").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()