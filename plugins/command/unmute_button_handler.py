
from pyrogram import Client, filters, types
import config

@Client.on_callback_query(filters.regex(r"^unmute:(\d+)$"))
async def unmute_user(client: Client, callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    requester_id = callback.from_user.id

    if requester_id != user_id:
        return await callback.answer("❌ Kamu tidak bisa unmute orang lain.", show_alert=True)

    try:
        member = await client.get_chat_member(config.channel_1, requester_id)
        if member.status == "left":
            return await callback.answer("❌ Kamu belum join channel utama.", show_alert=True)

        await client.restrict_chat_member(
            chat_id=config.channel_2,
            user_id=requester_id,
            permissions=types.ChatPermissions(can_send_messages=True)
        )
        await callback.message.edit_text("✅ Kamu sudah join, dan sekarang sudah di-unmute.")
    except Exception as e:
        await callback.message.edit_text(f"Gagal unmute: {e}")
