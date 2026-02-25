# flight-price-watcher

This project automates the process of monitoring flight price drops by bridging Google Flights Email Alerts with Telegram Notifications using Google Apps Script. No external flight APIs or web scraping required.

🔄 How it Works
Google Flights: You set up a price alert for your desired route (e.g., Amsterdam to Shanghai).

Gmail: When a price change occurs, Google sends an alert email to your inbox.

Apps Script: A time-triggered script scans your Gmail for unread alerts from googleflights-noreply@google.com.

Telegram: The script parses the route and price, then sends an instant message to your Telegram bot.

🛠️ Setup Guide
1. Set up Google Flight Alerts
Go to Google Flights.

Search for your route (e.g., AMS to PVG) for July 17 – August 28.

Toggle the "Track prices" switch. Ensure your Gmail account is set to receive these notifications.

2. Create your Telegram Bot
Message @BotFather on Telegram.

Use /newbot to create your bot and save the API Token.

Message @userinfobot to get your personal Chat ID.

3. Configure Google Apps Script
Go to script.google.com and create a new project.

Paste the Code.gs (provided below) into the editor.

Replace YOUR_TELEGRAM_TOKEN and YOUR_CHAT_ID with your actual credentials.

4. Set the Automation Trigger
Click the Triggers (clock icon) in the sidebar.

Click + Add Trigger.

Function: checkFlightEmails | Event source: Time-driven | Type: Minutes timer | Interval: Every 30 minutes.
