from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import requests
from datetime import datetime


TOKEN = 'your_bot_token_here'
GOOGLE_APPS_SCRIPT_URL = 'your_google_apps_script_webhook_url'


user_sessions = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome! Please type 'go' (without quotes) to start submitting your price list."
    )

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()
    session = user_sessions.get(user_id, {})

    if text == "go":
        user_sessions[user_id] = {}
        update.message.reply_text("Great! Please send the price list (e.g., grainmeal K2200, etc).")
        return

    if session is not None:
        # If waiting for price list
        if "price_list" not in session:
            session["price_list"] = update.message.text
            user_sessions[user_id] = session
            update.message.reply_text(
                "Please enter the date the data was collected in dd/mm/yyyy format or type 'today' for current date."
            )
            return

        # If waiting for date input
        if "price_list" in session and "date" not in session:
            if text == "today":
                date_str = datetime.now().strftime("%d/%m/%Y")
            else:
                if not validate_date(text):
                    update.message.reply_text(
                        "Invalid date format. Please enter the date as dd/mm/yyyy or type 'today'."
                    )
                    return
                date_str = text

            session["date"] = date_str
            user_sessions[user_id] = session

            # Prepare data for submission
            data_to_send = prepare_data(session)
            try:
                r = requests.post(GOOGLE_APPS_SCRIPT_URL, json=data_to_send)
                if r.status_code == 200:
                    update.message.reply_text(f"✅ Data submitted successfully for {date_str}")
                else:
                    update.message.reply_text(f"❌ Failed to submit data. Error {r.status_code}")
            except Exception as e:
                update.message.reply_text(f"⚠️ Failed to connect to server. Error: {e}")

            user_sessions.pop(user_id, None)  # Clear session
            return

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def extract_price(text):
    for token in text.split():
        token = token.replace(",", "")
        if token.startswith("K") and token[1:].replace(" ", "").isdigit():
            return token[1:].replace(" ", "")
    return ""

def prepare_data(session):
    price_list = session.get("price_list", "")
    date_recorded = session.get("date", "")
    data = {
        "timestamp": datetime.now().isoformat(),
        "responder": "Danford",
        "dateRecorded": date_recorded,
        "grainmeal": "",
        "azam": "",
        "sugar": "",
        "soya": "",
        "oil": "",
        "eggs": "",
    }

    lines = price_list.splitlines()
    for line in lines:
        line_lower = line.lower()
        if "grainmeal" in line_lower:
            data["grainmeal"] = extract_price(line)
        elif "azam" in line_lower:
            data["azam"] = extract_price(line)
        elif "sugar" in line_lower:
            data["sugar"] = extract_price(line)
        elif "soya" in line_lower:
            data["soya"] = extract_price(line)
        elif "mafuta" in line_lower or "oil" in line_lower:
            data["oil"] = extract_price(line)
        elif "tray" in line_lower or "mazira" in line_lower:
            data["eggs"] = extract_price(line)

    return data

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
