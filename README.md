# 📦 Telegram Price List Bot

This is a simple Telegram bot that collects **market price data** via chat and automatically logs it to a **Google Sheet** using a **Google Apps Script webhook**.

It guides users through a step-by-step flow to:
1. Start a new session by typing `go`.
2. Submit a **price list** in free text (e.g., `grainmeal K2200, sugar K1800`).
3. Enter the **date** the prices were collected (or type `today`).
4. Automatically sends the parsed data to your backend.

---

## 🚀 Features

- ✅ Step-by-step guided data collection
- 🧠 Automatic parsing of price entries from free text
- 🗓️ Accepts manual date input or "today"
- 📤 Sends structured data (grainmeal, sugar, soya, eggs, etc.) to a Google Apps Script endpoint
- 💬 Easy to use via Telegram

---

## 📊 Sample Data Flow

User: go
Bot: Great! Please send the price list (e.g., grainmeal K2200, etc).

User: grainmeal K2200, sugar K1800, eggs K3500
Bot: Please enter the date the data was collected in dd/mm/yyyy format or type 'today'.

User: today
Bot: ✅ Data submitted successfully for 28/06/2025
