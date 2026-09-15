# 👑 Cleydo Admins
ADMINS = {"https://www.facebook.com/share/1Zb1n5SYo6/"}

def is_admin(user_id):
    return str(user_id) in ADMINS

def admin_add_money(admin_id, target_id, amount):
    if not is_admin(admin_id):
        return "❌ You don't have permission to use this command."

    if amount <= 0:
        return "❌ Amount must be greater than 0."

    add_money(target_id, amount)

    return f"👑 Added **{amount:,} coins** to {target_id}."


def admin_remove_money(admin_id, target_id, amount):
    if not is_admin(admin_id):
        return "❌ You don't have permission to use this command."

    if amount <= 0:
        return "❌ Amount must be greater than 0."

    wallet, bank = get_balance(target_id)

    if wallet + bank < amount:
        return "❌ That user doesn't have enough money."

    # Remove from wallet first
    wallet_remove = min(wallet, amount)
    remaining = amount - wallet_remove

    db = connect()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE users
        SET wallet = wallet - ?,
            bank = bank - ?
        WHERE user_id = ?
    """, (wallet_remove, remaining, str(target_id)))

    db.commit()
    db.close()

    return f"👑 Removed **{amount:,} coins** from {target_id}."
