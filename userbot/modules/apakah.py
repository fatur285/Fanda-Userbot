# © copyright by emiko robot

import random
from userbot.utils import fanda_cmd

APAKAH_STRING = ["Iya", 
                 "Tidak", 
                 "Mungkin", 
                 "Mungkin Tidak", 
                 "Bisa jadi", 
                 "Mungkin Tidak",
                 "Tidak Mungkin",
                 "YNTKTS",
                 "Pala bapak kau pecah",
                 "Apa iya?",
                 "Tanya aja sama mamak kau tu pler"
                 ]


@fanda_cmd(pattern="apakah ?(.*)")
async def apakah(naon):
    quew = event.pattern_match.group(1)
    if not quew:
        await naon.reply('Berikan saya pertanyaan 😐')
        return
    await naon.reply(random.choice(APAKAH_STRING))
