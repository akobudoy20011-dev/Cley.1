import random


# =========================
# BLACKJACK
# =========================

def blackjack():
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K"]

    player = [random.choice(cards), random.choice(cards)]
    dealer = [random.choice(cards), random.choice(cards)]

    return (
        "🃏 BLACKJACK\n\n"
        f"Your cards: {' | '.join(player)}\n"
        f"Dealer's cards: {dealer[0]} | ❓\n\n"
        "Type `cleydo hit` or `cleydo stand`."
    )


# =========================
# UNO
# =========================

def uno():
    colors = ["🔴", "🟡", "🟢", "🔵"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    card1 = random.choice(colors) + random.choice(numbers)
    card2 = random.choice(colors) + random.choice(numbers)
    card3 = random.choice(colors) + random.choice(numbers)

    return (
        "🃏 UNO\n\n"
        f"Your cards:\n"
        f"1️⃣ {card1}\n"
        f"2️⃣ {card2}\n"
        f"3️⃣ {card3}\n\n"
        "Type `cleydo play 1` to play a card!"
    )


# =========================
# COIN FLIP
# =========================

def coinflip():
    result = random.choice(["🪙 HEADS", "🪙 TAILS"])

    return f"🪙 Cleydo flipped a coin!\n\n{result}"


# =========================
# HUNT
# =========================

def hunt():
    animals = [
        ("🐰 Rabbit", 20, 60),
        ("🦊 Fox", 40, 90),
        ("🐺 Wolf", 60, 120),
        ("🐻 Bear", 80, 160),
        ("🦌 Deer", 50, 100)
    ]

    animal, minimum, maximum = random.choice(animals)
    coins = random.randint(minimum, maximum)

    return (
        f"🏹 You went hunting!\n\n"
        f"You found a {animal}!\n"
        f"💰 +{coins} coins"
    )


# =========================
# DICE
# =========================

def dice():
    number = random.randint(1, 6)

    return (
        "🎲 DICE\n\n"
        f"You rolled: **{number}**"
    )


# =========================
# SLOTS
# =========================

def slots():
    symbols = ["🍒", "🍋", "🍇", "⭐", "💎", "🔔"]

    a = random.choice(symbols)
    b = random.choice(symbols)
    c = random.choice(symbols)

    result = f"{a} | {b} | {c}"

    if a == b == c:
        return (
            f"🎰 {result}\n\n"
            "✨ THREE MATCH!\n"
            "🎉 JACKPOT!"
        )

    elif a == b or b == c or a == c:
        return (
            f"🎰 {result}\n\n"
            "✨ TWO MATCH!"
        )

    else:
        return (
            f"🎰 {result}\n\n"
            "Nothing matched 😭"
        )
