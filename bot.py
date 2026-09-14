from flask import Flask, request
import requests
import os

from money import (
    get_balance,
    deposit,
    withdraw,
    daily
)

from permissions import can_announce

app = Flask(__name__)

# These will be added in Render later
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")


# =========================
# CLEyDO COMMANDS
# =========================

def cleydo(message, user_id):
    message = message.lower().strip()

    if not message.startswith("cleydo"):
        return None

    command = message[6:].strip()

    # HELP
    if command == "help":
        return (
            "🐈‍⬛ Cleydo Commands\n\n"
            "💰 cleydo balance\n"
            "🎁 cleydo daily\n"
            "🏦 cleydo deposit <amount>\n"
            "💵 cleydo withdraw <amount>\n"
            "📢 cleydo announce <message>"
        )

    # BALANCE
    elif command == "balance":
        wallet, bank = get_balance(user_id)

        return (
            "💰 Your Cleydo Balance\n\n"
            f"👛 Wallet: {wallet:,} coins\n"
            f"🏦 Bank: {bank:,} coins\n"
            f"💎 Total: {wallet + bank:,} coins"
        )

    # DAILY
    elif command == "daily":
        return daily(user_id)

    # DEPOSIT
    elif command.startswith("deposit "):
        try:
            amount = int(command.split()[1])
            return deposit(user_id, amount)
        except (ValueError, IndexError):
            return "❌ Usage: `cleydo deposit <amount>`"

    # WITHDRAW
    elif command.startswith("withdraw "):
        try:
            amount = int(command.split()[1])
            return withdraw(user_id, amount)
        except (ValueError, IndexError):
            return "❌ Usage: `cleydo withdraw <amount>`"

    # ANNOUNCEMENT
    elif command.startswith("announce "):
        announcement = command[9:].strip()

        if not can_announce(user_id):
            return "❌ Only the admin can make announcements."
        if not announcement:
            return "❌ Write an announcement."

        return (
            "🐈‍⬛・ANNOUNCEMENT\n\n"
            f"{announcement}\n\n"
            "🐾"
        )

    # UNKNOWN COMMAND
    else:
        return "❓ Unknown command. Try `cleydo help`."


# =========================
# SEND MESSAGE TO MESSENGER
# =========================

def send_message(recipient_id, text):
    url = (
        "https://graph.facebook.com/v23.0/me/messages"
        f"?access_token={PAGE_ACCESS_TOKEN}"
    )

    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        }
    }

    requests.post(url, json=data)


# =========================
# FACEBOOK WEBHOOK
# =========================

@app.route("/webhook", methods=["GET"])
def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if data.get("object") == "page":

        for entry in data.get("entry", []):

            for messaging_event in entry.get("messaging", []):

                sender = messaging_event.get("sender", {})
                sender_id = sender.get("id")

                message = messaging_event.get("message", {})
                text = message.get("text")

                if sender_id and text:

                    response = cleydo(
                        text,
                        sender_id
                    )

                    if response:
                        send_message(
                            sender_id,
                            response
                        )

        return "EVENT_RECEIVED", 200

    return "Not a page event", 404


# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
