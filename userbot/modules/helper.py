""" Userbot module for other small commands. """
from userbot import CMD_HELP, ALIVE_NAME, CMD_HANDLER as cmd
from userbot.utils import fanda_cmd


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@fanda_cmd(pattern="helpmy$")
async def usit(e):
    await e.edit(
        f"**Halo {DEFAULTUSER} jika kamu tidak tahu perintah untuk memerintahku ketik** `.help` **atau minta bantuan kepada:**\n"
        "\n[Fatur](t.me/uurfavboys)"
        "\n[Support](t.me/fandasupport)"
        "\n[Instagram](instagram.com/fatur.285)")


@fanda_cmd(pattern="vars$")
async def var(m):
    await m.edit(
        f"**Daftar Vars Dari {DEFAULTUSER}:**\n"
        "\n[ [klik disini](https://raw.githubusercontent.com/DIORrios285/Fanda-Userbot/main/varshelper.txt) ]")


CMD_HELP.update({
    "helper":
    "`{cmd}lhelp`\
\nUsage: Bantuan Untuk Fanda-Userbot.\
\n`{cmd}vars`\
\nUsage: Melihat Daftar Vars."
})
