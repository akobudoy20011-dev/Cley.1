import os


# =========================================================
# ADMINS
# =========================================================

ADMINS = {
    admin_id.strip()
    for admin_id in os.environ.get(
        "ADMIN_IDS",
        "",
    ).split(",")
    if admin_id.strip()
}


# =========================================================
# ADMIN CHECK
# =========================================================

def is_admin(user_id):
    return str(user_id) in ADMINS


def can_announce(user_id):
    return is_admin(user_id)
