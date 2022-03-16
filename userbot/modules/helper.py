""" Userbot module for other small commands. """
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, fanda_cmd


@fanda_cmd(pattern="ihelp$")
async def usit(event):
    me = await event.client.get_me()
    await edit_or_reply(
        event,
        f"**Hai {me.first_name} Kalo Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.help` Atau Bisa Minta Bantuan Ke:\n"
        f"✣ **Group Support :** [Fanda Support](t.me/fandasupport)\n"
        f"✣ **Channel fanda :** [Fanda Project](t.me/fandaproject)\n"
        f"✣ **Owner Repo :** [Fatur](t.me/uurfavboys)\n"
        f"✣ **Repo :** [Fanda-Userbot](https://github.com/DIORrios285/Fanda-Userbot)\n",
    )


@fanda_cmd(pattern="listvar$")
async def var(event):
    await edit_or_reply(
        event,
        "**Daftar Lengkap Vars Dari Fanda-Userbot:** [KLIK DISINI](https://raw.githubusercontent.com/DIORrios285/Fanda-Userbot/Fanda-Userbot/varshelper.txt)",
    )

CMD_HELP.update({
    "helper":
    "`{cmd}ihelp`\
\nUsage: Bantuan Untuk Fanda-Userbot.\
\n`{cmd}listvar`\
\nUsage: Melihat Daftar Vars."
})
