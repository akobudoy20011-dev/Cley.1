def cleydo(message):
    message = message.lower().strip()

    if not message.startswith("cleydo"):
        return None

    command = message[6:].strip()

    if command == "help":
        return "🤖 Cleydo Commands:\n\ncleydo profile\ncleydo balance\ncleydo daily\ncleydo hunt"

    elif command == "balance":
        return "💰 You have 100 coins!"

    elif command == "daily":
        return "🎁 Cleydo gave you 100 coins!"

    elif command == "hunt":
        return "🏹 You went hunting and found 75 coins!"

    elif command == "profile":
        return "👤 Your Cleydo profile\n💰 Coins: 100\n⭐ Level: 1"

    else:
        return "❓ I don't know that command. Try `cleydo help`."
