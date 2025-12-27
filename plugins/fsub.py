from config import FORCE_CHANNEL_ID, FORCE_CHANNEL_USERNAME
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest


def check_force_sub(update, context):
    """
    Returns True if user is subscribed
    Returns False and sends join message if not subscribed
    """

    if FORCE_CHANNEL_ID == 0:
        return True

    user = update.effective_user
    if not user:
        return True

    try:
        member = context.bot.get_chat_member(
            chat_id=FORCE_CHANNEL_ID,
            user_id=user.id
        )
        if member.status in ["member", "administrator", "creator"]:
            return True
    except BadRequest:
        pass

    buttons = [
        [InlineKeyboardButton("📢 Join Channel", url=FORCE_CHANNEL_USERNAME)],
        [InlineKeyboardButton("✅ Recheck", callback_data="fsub_recheck")]
    ]

    text = (
        "🚫 **You must join our channel to use this bot**\n\n"
        "👉 Join the channel first\n"
        "👉 Then press **Recheck**"
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
