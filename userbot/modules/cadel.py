import random
from userbot import owner
from telethon.tl.types import InputMessagesFilterVideo
from telethon.tl.types import InputMessagesFilterVoice
from userbot import CMD_HELP
from userbot import CMD_HANDLER as cmd
from userbot.utils import fanda_cmd


@fanda_cmd(pattern="cadel$")
async def _(event):
    try:
        rrrr = [
            rrrrrr
            async for asupan in event.client.iter_messages(
                "@sicadelini", filter=InputMessagesFilterVoice
            )
        ]
        await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(rrrr),
            caption=f"**Nih banh**.")
        
        await event.delete()
    except Exception:
        await event.edit("Tidak bisa menemukan voice msg.")

        

CMD_HELP.update(
    {
        "cadel": f"**Plugin : **`cadel`\
        \n\n  •  **Syntax :** `{cmd}cadel`\
        \n  •  **Function : **Cobain aja.\
    "
    }
)
