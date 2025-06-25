import config
from pyrogram import Client, types, enums
from plugins import Helper
from plugins.database import Database  # pastikan ini sesuai struktur foldermu

async def start_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    user_id = msg.from_user.id
    db = Database(user_id)

    # Cek apakah user sudah jadi member
    if not await db.is_member():
        text = (
            "🚫 KAMU TIDAK TERDAFTAR SEBAGAI MEMBER.\n\n"
            "Silakan hubungi admin untuk mendaftar menjadi member.\n"
            "Biaya pendaftaran: Rp 2.000"
        )
        await msg.reply_photo(
            photo="https://telegra.ph/file/7dd90ea224c1eae8574c1.jpg",  # ganti dengan URL fotomu
            caption=text,
            quote=True
        )
        return

    # Jika member, kirim sambutan
    nama = msg.from_user.first_name
    await msg.reply_text(
        f"Hai {nama}, selamat datang di bot!",
        quote=True
    )
