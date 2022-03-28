# 🍀 © @tofik_dn
# ahh ahh udh pasti si fatur:)
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
# ⚠️ Do not remove credits

from secrets import choice

from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterVoice

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, fanda_cmd


@fanda_cmd(pattern="asupan$")
async def _(event):
    xx = await edit_or_reply(event, "`Tunggu Sebentar...`")
    try:
        asupannya = [
            asupan
            async for asupan in event.client.iter_messages(
                "@tedeasupancache", filter=InputMessagesFilterVideo
            )
        ]
        await event.client.send_file(
            event.chat_id, file=choice(asupannya), reply_to=event.reply_to_msg_id
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan video asupan.**")


@fanda_cmd(pattern="favsong$")
async def _(event):
    xx = await edit_or_reply(event, "`Tunggu Sebentar...`")
    try:
        favsong = [
            song
            async for song in event.client.iter_messages(
                "@uurfavsong", filter=InputMessagesFilterVoice
            )
        ]
        await event.client.send_file(
            event.chat_id, file=choice(favsong), reply_to=event.reply_to_msg_id
        )
        await xx.delete()
    except Exception:
        await xx.edit("**Tidak bisa menemukan fanda favorit song.**")


CMD_HELP.update(
    {
        "asupan": f"**Plugin : **`asupan`\
        \n\n  •  **Syntax :** `{cmd}asupan`\
        \n  •  **Function : **Untuk Mengirim video asupan secara random.\
    "
    }
)

CMD_HELP.update(
    {
        "fandafavsongs": f"**Plugin : **`favsong`\
        \n\n  •  **Syntax :** `{cmd}favsong`\
        \n  •  **Function : **Kumpulan lagu favorit dari owner Fanda-Userbot.\
    "
    }
)
