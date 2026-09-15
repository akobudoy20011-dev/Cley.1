# permissions.py

ADMINS = {"https://www.facebook.com/share/1Zb1n5SYo6/"}

def is_admin(user_id):
    return str(user_id) in ADMINS

def can_announce(user_id):
    return is_admin(user_id)
