
from pyrogram import Client, filters, types
import config

@Client.on_message(filters.channel & filters.reply & filters.chat(config.channel_1))
async def notif_komentar(client: Client, msg: types.Message):
    try:
        original = msg.reply_to_message
        if original.forward_from:
            sender_id = original.forward_from.id
            await client.send_message(
                sender_id,
                "💬 Pesan kamu baru saja dikomentari oleh seseorang di channel."
            )
    except Exception as e:
        print(f"[komen_notif_handler] Gagal kirim notifikasi: {e}")
