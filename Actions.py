ACTIONS = {
    "slap": {
        "text": "{user} slapped {target}! 👋",
        "gif": "gifs/slap.gif"
    },

    "kick": {
        "text": "{user} kicked {target}! 🦵",
        "gif": "gifs/kick.gif"
    },

    "punch": {
        "text": "{user} punched {target}! 👊",
        "gif": "gifs/punch.gif"
    },

    "hug": {
        "text": "{user} hugged {target}! 🫂",
        "gif": "gifs/hug.gif"
    },

    "pat": {
        "text": "{user} patted {target}! 🫳",
        "gif": "gifs/pat.gif"
    },

    "highfive": {
        "text": "{user} high-fived {target}! 🙌",
        "gif": "gifs/highfive.gif"
    },

    "poke": {
        "text": "{user} poked {target}! 👉",
        "gif": "gifs/poke.gif"
    }
}


def action(command, user):
    parts = command.strip().split(maxsplit=1)

    if len(parts) < 2:
        return {
            "text": "❌ Mention someone!\nExample: cleydo slap @John"
        }

    action_name = parts[0].lower()
    target = parts[1].strip()

    if action_name not in ACTIONS:
        return {
            "text": "❌ That action doesn't exist!"
        }

    if not target.startswith("@"):
        return {
            "text": "❌ You need to mention someone!"
        }

    data = ACTIONS[action_name]

    return {
        "text": data["text"].format(
            user=user,
            target=target
        ),
        "gif": data["gif"]
    }
