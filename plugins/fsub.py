from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

from config import FSUB_CHANNELS


async def get_fsub_channels():
    return FSUB_CHANNELS


async def check_subscription_status(client, user_id, channels):
    not_joined = []

    for channel in channels:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in (
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ):
                not_joined.append(channel)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            pass

    if not not_joined:
        return True, None, None

    buttons = []

    for ch in not_joined:
        buttons.append([
            InlineKeyboardButton(
                "📢 Join ANIME IN HINDI",
                url="https://t.me/Lite_Anime_Hindi"
            )
        ])

    buttons.append([
        InlineKeyboardButton("✅ Check Again", callback_data="check_sub")
    ])

    text = (
        "<b>🚨 ACCESS DENIED!</b>\n\n"
        "You must join <b>ANIME IN HINDI</b> channel to use this bot.\n\n"
        "👇 Join the channel and then click <b>Check Again</b>"
    )

    return False, text, InlineKeyboardMarkup(buttons)        "👉 Then press **Recheck**"
    )

    if update.message:
        update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )
    elif update.callback_query:
        update.callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )

    return False


def fsub_recheck(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    try:
        member = context.bot.get_chat_member(FORCE_CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            query.message.edit_text(
                "✅ Subscription verified!\n\nSend /start again 🚀"
            )
            return
    except BadRequest:
        pass

    query.answer("❌ You haven't joined yet!", show_alert=True)
