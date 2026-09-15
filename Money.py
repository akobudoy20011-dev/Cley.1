import sqlite3
import time
import os

# =========================
# DATABASE
# =========================

DB_FILE = "cleydo.db"


def connect():
    db = sqlite3.connect(DB_FILE)

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            wallet INTEGER NOT NULL DEFAULT 0,
            bank INTEGER NOT NULL DEFAULT 0,
            last_daily INTEGER NOT NULL DEFAULT 0
        )
    """)

    db.commit()
    return db


def ensure_user(user_id):
    user_id = str(user_id)

    db = connect()
    cursor = db.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )

    db.commit()
    db.close()


# =========================
# BALANCE
# =========================

def get_balance(user_id):
    ensure_user(user_id)

    db = connect()
    cursor = db.cursor()

    cursor.execute(
        "SELECT wallet, bank FROM users WHERE user_id = ?",
        (str(user_id),)
    )

    result = cursor.fetchone()
    db.close()

    if result is None:
        return 0, 0

    return result[0], result[1]


# =========================
# ADD MONEY
# =========================

def add_money(user_id, amount):
    ensure_user(user_id)

    db = connect()

    db.execute(
        "UPDATE users SET wallet = wallet + ? WHERE user_id = ?",
        (amount, str(user_id))
    )

    db.commit()
    db.close()


# =========================
# DEPOSIT
# =========================

def deposit(user_id, amount):
    if amount <= 0:
        return "❌ Amount must be greater than 0."

    wallet, bank = get_balance(user_id)

    if wallet < amount:
        return "❌ You don't have enough coins in your wallet."

    db = connect()

    db.execute("""
        UPDATE users
        SET wallet = wallet - ?,
            bank = bank + ?
        WHERE user_id = ?
    """, (amount, amount, str(user_id)))

    db.commit()
    db.close()

    return (
        f"🏦 Deposited **{amount:,} coins**.\n\n"
        f"👛 Wallet: {wallet - amount:,}\n"
        f"🏦 Bank: {bank + amount:,}"
    )


# =========================
# WITHDRAW
# =========================

def withdraw(user_id, amount):
    if amount <= 0:
        return "❌ Amount must be greater than 0."

    wallet, bank = get_balance(user_id)

    if bank < amount:
        return "❌ You don't have enough coins in your bank."

    db = connect()

    db.execute("""
        UPDATE users
        SET wallet = wallet + ?,
            bank = bank - ?
        WHERE user_id = ?
    """, (amount, amount, str(user_id)))

    db.commit()
    db.close()

    return (
        f"💵 Withdrew **{amount:,} coins**.\n\n"
        f"👛 Wallet: {wallet + amount:,}\n"
        f"🏦 Bank: {bank - amount:,}"
    )


# =========================
# DAILY
# =========================

DAILY_AMOUNT = 500
DAILY_COOLDOWN = 24 * 60 * 60


def daily(user_id):
    ensure_user(user_id)

    db = connect()
    cursor = db.cursor()

    cursor.execute(
        "SELECT last_daily FROM users WHERE user_id = ?",
        (str(user_id),)
    )

    result = cursor.fetchone()
    last_daily = result[0] if result else 0

    now = int(time.time())
    remaining = DAILY_COOLDOWN - (now - last_daily)

    if remaining > 0:
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        return (
            "🎁 You already claimed your daily reward!\n"
            f"⏰ Try again in {hours}h {minutes}m."
        )

    cursor.execute("""
        UPDATE users
        SET wallet = wallet + ?,
            last_daily = ?
        WHERE user_id = ?
    """, (DAILY_AMOUNT, now, str(user_id)))

    db.commit()
    db.close()

    return (
        "🎁 DAILY REWARD!\n\n"
        f"💰 You received **{DAILY_AMOUNT:,} coins**!"
    )


# =========================
# ADMIN SYSTEM
# =========================

ADMINS = {
    "https://www.facebook.com/share/1Zb1n5SYo6/"
}


def is_admin(user_id):
    return str(user_id) in ADMINS


# =========================
# ADMIN ADD MONEY
# =========================

def admin_add_money(admin_id, target_id, amount):
    if not is_admin(admin_id):
        return "❌ You don't have permission to use this command."

    if amount <= 0:
        return "❌ Amount must be greater than 0."

    add_money(target_id, amount)

    return (
        f"👑 Added **{amount:,} coins** to {target_id}."
    )


# =========================
# ADMIN REMOVE MONEY
# =========================

def admin_remove_money(admin_id, target_id, amount):
    if not is_admin(admin_id):
        return "❌ You don't have permission to use this command."

    if amount <= 0:
        return "❌ Amount must be greater than 0."

    wallet, bank = get_balance(target_id)

    if wallet + bank < amount:
        return "❌ That user doesn't have enough money."

    wallet_remove = min(wallet, amount)
    remaining = amount - wallet_remove

    db = connect()

    db.execute("""
        UPDATE users
        SET wallet = wallet - ?,
            bank = bank - ?
        WHERE user_id = ?
    """, (
        wallet_remove,
        remaining,
        str(target_id)
    ))

    db.commit()
    db.close()

    return (
        f"👑 Removed **{amount:,} coins** from {target_id}."
    )
