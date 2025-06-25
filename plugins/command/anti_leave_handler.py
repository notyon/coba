
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

@Client.on_message(filters.group & filters.chat(config.channel_2))
async def check_subscription(client: Client, msg: types.Message):
    user = msg.from_user
    try:
        member = await client.get_chat_member(config.channel_1, user.id)
        if member.status == "left":
            await client.restrict_chat_member(
                chat_id=config.channel_2,
                user_id=user.id,
                permissions=types.ChatPermissions()  # mute total
            )
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔓 Unmute Saya", callback_data=f"unmute:{user.id}")]]
            )
            await msg.reply(
                f"🚫 Kamu harus join ke {config.channel_1} untuk bisa kirim pesan di grup.",
                reply_markup=keyboard
            )
    except Exception as e:
        print(f"[anti_leave_handler] Error: {e}")
