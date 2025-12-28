from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from config import FORCE_SUB_CHANNEL

async def get_fsub_channels():
    """
    Returns force subscribe channel(s)
    """
    return [FORCE_SUB_CHANNEL]


async def check_subscription_status(client: Client, user_id: int) -> bool:
    """
    Check if user is member of force subscribe channel
    """
    try:
        await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return False
