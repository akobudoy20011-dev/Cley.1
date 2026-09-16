import random

from Money import add_money


# =========================
# GAME SETTINGS
# =========================

HUNT_MIN_REWARD = 20
HUNT_MAX_REWARD = 160


# =========================
# BLACKJACK
# =========================

CARDS = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
]


def card_value(card):
    if card == "A":
        return 11

    if card in ("J", "Q", "K"):
        return 10

    return int(card)


def hand_value(hand):
    total = sum(card_value(card) for card in hand)
    aces = hand.count("A")

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def blackjack():
    player = [
        random.choice(CARDS),
        random.choice(CARDS),
    ]

    dealer = [
        random.choice(CARDS),
        random.choice(CARDS),
    ]

    player_total = hand_value(player)

    # Natural blackjack
    if player_total == 21:
        return (
            "╭───────────────╮\n"
            "   🃏 BLACKJACK\n"
            "╰───────────────╯\n\n"
            f"Your cards: {' | '.join(player)}\n"
            f"Your total: **{player_total}**\n\n"
            f"Dealer: {dealer[0]} | ❓\n\n"
            "✨ NATURAL BLACKJACK!\n"
            "You need a game session to continue with hit/stand."
        )

    return (
        "╭───────────────╮\n"
        "   🃏 BLACKJACK\n"
        "╰───────────────╯\n\n"
        f"Your cards: {' | '.join(player)}\n"
        f"Your total: **{player_total}**\n\n"
        f"Dealer: {dealer[0]} | ❓\n\n"
        "🎴 `cleydo hit`\n"
        "🛑 `cleydo stand`"
    )


# =========================
# UNO
# =========================

UNO_COLORS = [
    "🔴",
    "🟡",
    "🟢",
    "🔵",
]

UNO_NUMBERS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


def generate_uno_card():
    return (
        random.choice(UNO_COLORS)
        + random.choice(UNO_NUMBERS)
    )


def uno():
    cards = [
        generate_uno_card(),
        generate_uno_card(),
        generate_uno_card(),
    ]

    return (
        "╭───────────────╮\n"
        "      🃏 UNO\n"
        "╰───────────────╯\n\n"
        "Your cards:\n\n"
        f"1️⃣ {cards[0]}\n"
        f"2️⃣ {cards[1]}\n"
        f"3️⃣ {cards[2]}\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "Play a card with:\n"
        "`cleydo play 1`\n"
        "`cleydo play 2`\n"
        "`cleydo play 3`"
    )


# =========================
# COIN FLIP
# =========================

def coinflip():
    result = random.choice([
        "🪙 HEADS",
        "🪙 TAILS",
    ])

    return (
        "╭───────────────╮\n"
        "   🪙 COIN FLIP\n"
        "╰───────────────╯\n\n"
        "Cleydo flipped the coin...\n\n"
        f"✨ **{result}**"
    )


# =========================
# HUNT
# =========================

ANIMALS = [
    ("🐰 Rabbit", 20, 60),
    ("🦊 Fox", 40, 90),
    ("🐺 Wolf", 60, 120),
    ("🐻 Bear", 80, 160),
    ("🦌 Deer", 50, 100),
]


def hunt(user_id):
    animal, minimum, maximum = random.choice(ANIMALS)

    coins = random.randint(
        minimum,
        maximum,
    )

    add_money(
        user_id,
        coins,
    )

    return (
        "╭───────────────╮\n"
        "     🏹 HUNT\n"
        "╰───────────────╯\n\n"
        f"You encountered a {animal}!\n\n"
        f"💰 **+{coins:,} coins**\n\n"
        "The hunt has been added to your wallet."
    )


# =========================
# DICE
# =========================

def dice():
    number = random.randint(
        1,
        6,
    )

    dice_faces = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅",
    }

    face = dice_faces[number]

    return (
        "╭───────────────╮\n"
        "      🎲 DICE\n"
        "╰───────────────╯\n\n"
        f"{face}  **{number}**\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "Luck has spoken."
    )


# =========================
# SLOTS
# =========================

SLOT_SYMBOLS = [
    "🍒",
    "🍋",
    "🍇",
    "⭐",
    "💎",
    "🔔",
]


def slots():
    a = random.choice(SLOT_SYMBOLS)
    b = random.choice(SLOT_SYMBOLS)
    c = random.choice(SLOT_SYMBOLS)

    result = f"{a} │ {b} │ {c}"

    if a == b == c:
        outcome = (
            "✨ **THREE MATCH!**\n"
            "🎉 JACKPOT!"
        )

    elif a == b or b == c or a == c:
        outcome = (
            "✨ **TWO MATCH!**\n"
            "Not bad!"
        )

    else:
        outcome = (
            "Nothing matched.\n"
            "Better luck next time. 😭"
        )

    return (
        "╭─────────────────╮\n"
        "      🎰 SLOTS\n"
        "╰─────────────────╯\n\n"
        f"      {result}\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        f"{outcome}"
    )


# =========================
# GAME ROUTER
# =========================

def play_game(game_name, user_id=None):
    game_name = str(game_name).lower().strip()

    if game_name == "blackjack":
        return blackjack()

    if game_name == "uno":
        return uno()

    if game_name in ("coinflip", "coin", "flip"):
        return coinflip()

    if game_name == "hunt":
        if user_id is None:
            return "❌ User ID is required for hunting."

        return hunt(user_id)

    if game_name in ("dice", "roll"):
        return dice()

    if game_name == "slots":
        return slots()

    return (
        "❌ Unknown game.\n\n"
        "Available games:\n"
        "🃏 blackjack\n"
        "🃏 uno\n"
        "🪙 coinflip\n"
        "🏹 hunt\n"
        "🎲 dice\n"
        "🎰 slots"
    )


# =========================
# GAME HELP
# =========================

def game_help():
    return (
        "╭──────────────────╮\n"
        "      🎮 CLEYDO GAMES\n"
        "╰──────────────────╯\n\n"
        "🃏 `cleydo blackjack`\n"
        "Play Blackjack.\n\n"
        "🃏 `cleydo uno`\n"
        "Draw your UNO hand.\n\n"
        "🪙 `cleydo coinflip`\n"
        "Flip a coin.\n\n"
        "🏹 `cleydo hunt`\n"
        "Go hunting for coins.\n\n"
        "🎲 `cleydo dice`\n"
        "Roll a six-sided die.\n\n"
        "🎰 `cleydo slots`\n"
        "Spin the slot machine."
    )
