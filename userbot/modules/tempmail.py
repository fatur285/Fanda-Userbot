from telethon import events
from userbot import OWNER, CMD_HELP, bot, CMD_HANDLER as cmd
from userbot.utils import fanda_cmd
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio


@fanda_cmd(pattern="tm(?: |$)(.*)")
async def _(event):
    chat = "@TempMailBot"
    geez = await event.edit("Sedang Memprosess...")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True,
                from_users=OWNER
            )
            )
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("Generate New")
            response = await response
            geezuserbot = ((response).reply_markup.rows[2].buttons[0].url)
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await geez.edit("`Mohon Maaf, Silahkan Buka` @TempMailBot `Lalu Tekan Start dan Coba Lagi.`")
            return
        await event.edit(f"**GEEZ TEMPMAIL** ~ `{response.message.message}`\n\n[KLIK DISINI UNTUK VERIFIKASI]({geezuserbot})")


CMD_HELP.update({"tempmail": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{cmd}tm`"
                 "\n•: Mendapatkan Email Gratis Dari Temp Mail"})
