from telethon import Button

from userbot import BOTLOG, BOTLOG_CHATID, LOGS, tgbot


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            await tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/8ee507ef2468557fc49e0.jpg",
                caption="**Fanda-Userbot started**!\n\n**Python:** `3.9.10`\n**Pyrogram:** `1.4.8`\n**PyTgCalls:** `0.9.0 Beta 1`",
                buttons=[(Button.url("ꜱᴜᴘᴘᴏʀᴛ", "https://t.me/Fandasupport"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
