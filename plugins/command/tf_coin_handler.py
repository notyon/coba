
from pyrogram import Client, filters, types, enums
from plugins.database import Database
import config

@Client.on_message(filters.command("tf_coin") & filters.group)
async def tf_coin_handler(client: Client, msg: types.Message):
    if not msg.reply_to_message:
        return await msg.reply("❌ Balas pesan orang yang ingin kamu transfer koinnya. Contoh: /tf_coin 10")
    
    target_id = msg.reply_to_message.from_user.id
    sender_id = msg.from_user.id

    if target_id == sender_id:
        return await msg.reply("❌ Kamu tidak bisa transfer ke diri sendiri.")

    try:
        jumlah = int(msg.command[1])
        if jumlah <= 0:
            raise ValueError
    except:
        return await msg.reply("❌ Jumlah koin tidak valid. Gunakan: /tf_coin <jumlah>")

    db_sender = Database(sender_id)
    db_target = Database(target_id)

    if not await db_sender.kurangi_coin(jumlah):
        return await msg.reply("❌ Koin kamu tidak cukup.")

    
    fee = max(1, jumlah // 100)  # minimal fee 1 koin
    jumlah_bersih = jumlah - fee
    await db_target.tambah_coin(jumlah_bersih)
    await Database(config.OWNER_ID).tambah_coin(fee)
    
    await msg.reply(
        f"✅ Berhasil transfer {jumlah_bersih} coin ke user {target_id}.\n💸 Fee 1% ({fee} coin) masuk ke admin.",
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )
