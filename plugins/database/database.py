import pymongo
import config
import json
from datetime import datetime

myclient = pymongo.MongoClient(config.db_url)
mydb = myclient[config.db_name]
mycol = mydb['user']


class Database:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def tambah_databot(self):
        data = {
            "_id": self.user_id,
            "nama": "Pengguna",
            "status": f"nonmember_{self.user_id}",
            "coin": f"0_{self.user_id}",
            "menfess": 0,
            "all_menfess": 0,
            "sign_up": datetime.utcnow().isoformat(),
            "bot_status": True,
            "ban": {},
            "admin": [],
            "kirimchannel": {
                "photo": True,
                "video": False,
                "voice": False
            }
        }
        await self.tambah_pelanggan(data)

    async def cek_user_didatabase(self):
        found = mycol.find_one({'_id': self.user_id})
        return found is not None

    async def tambah_pelanggan(self, data):
        mycol.insert_one(data)

    async def hapus_pelanggan(self, user_id: int):
        mycol.delete_one({'_id': user_id})

    async def update_menfess(self, coin: int, menfess: int, all_menfess: int):
        user = self.get_data_pelanggan()
        last_coin = user.coin
        last_menfess = user.menfess
        last_all_menfess = user.all_menfess
        mycol.update_one(
            {"coin": f"{last_coin}_{str(user.id)}", "menfess": last_menfess, "all_menfess": last_all_menfess},
            {"$set": {
                "coin": f"{coin}_{str(user.id)}",
                "menfess": (menfess + 1),
                "all_menfess": (all_menfess + 1)}
            }
        )

    async def reset_menfess(self):
        new = {"$set": {"menfess": 0}}
        x = mycol.update_many({}, new)
        return x.modified_count

    async def transfer_coin(self, ditranfer: int, diterima: int, coin_awal_target_full: int, id_target: int):
        coin_awal_user = self.get_data_pelanggan().coin_full
        mycol.update_one(
            {"coin": coin_awal_user},
            {"$set": {"coin": f"{ditranfer}_{self.user_id}"}}
        )
        mycol.update_one(
            {"coin": coin_awal_target_full},
            {"$set": {"coin": f"{diterima}_{id_target}"}}
        )

    async def get_coin(self) -> int:
        user = mycol.find_one({'_id': self.user_id})
        return int(user['coin'].split('_')[0]) if user else 0

    async def kurangi_coin(self, jumlah: int) -> bool:
        user = mycol.find_one({'_id': self.user_id})
        current = int(user['coin'].split('_')[0])
        if user and current >= jumlah:
            mycol.update_one({'_id': self.user_id}, {"$set": {"coin": f"{current - jumlah}_{self.user_id}"}})
            return True
        return False

    async def tambah_coin(self, jumlah: int):
        user = mycol.find_one({'_id': self.user_id})
        current = int(user['coin'].split('_')[0])
        mycol.update_one({'_id': self.user_id}, {"$set": {"coin": f"{current + jumlah}_{self.user_id}"}})

    def get_pelanggan(self):
        user_ids = [doc['_id'] for doc in mycol.find()]
        return get_pelanggan(user_ids)

    def get_data_pelanggan(self):
        found = mycol.find_one({'_id': self.user_id})
        return data_pelanggan(found)

    def get_data_bot(self, id_bot):
        found = mycol.find_one({'_id': id_bot})
        return data_bot(found)


class get_pelanggan:
    def __init__(self, ids: list):
        if ids:
            ids.remove(ids[0])
        self.total_pelanggan = len(ids)
        self.id_pelanggan = ids
        self.json = {"total_pelanggan": len(ids), "id_pelanggan": ids}

    def get_data_pelanggan(self, index: int = 0):
        found = mycol.find_one({'_id': self.id_pelanggan[index]})
        return data_pelanggan(found) if found else 'ID tidak ditemukan'

    def __str__(self):
        return json.dumps(self.json, indent=3)


class data_pelanggan:
    def __init__(self, args):
        self.id = args['_id']
        self.nama = str(args['nama'])
        self.mention = f'<a href="tg://user?id={self.id}">{self.nama}</a>'
        self.coin = int(args['coin'].split('_')[0])
        self.coin_full = str(args['coin'])
        self.status = str(args['status'].split('_')[0])
        self.status_full = str(args['status'])
        self.menfess = int(args['menfess'])
        self.all_menfess = int(args['all_menfess'])
        self.sign_up = args['sign_up']
        self.json = args

    def __str__(self):
        return json.dumps(self.json, indent=3)


class data_bot:
    def __init__(self, args):
        self.id = args['_id']
        self.bot_status = args['bot_status']
        self.ban = dict(args['ban'])
        self.admin = list(args['admin'])
        self.kirimchannel = kirim_channel(dict(args['kirimchannel']))
        self.json = args

    def __str__(self):
        return json.dumps(self.json, indent=3)


class kirim_channel:
    def __init__(self, args):
        self.photo = args['photo']
        self.video = args['video']
        self.voice = args['voice']
        self.json = args

    def __str__(self):
        return json.dumps(self.json, indent=3)
        
