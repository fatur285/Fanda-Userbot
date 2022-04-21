# rewrite by {}

from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from telethon.tl import types
from telethon.utils import get_display_name

from userbot import CMD_HANDLER as nothing
from userbot import CMD_HELP, call_py
from userbot.utils import edit_delete, edit_or_reply, fanda_cmd
from userbot.events import register

NO_ADMIN = "`Maaf Kamu Bukan Admin 👮`"


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


async def get_call(fuckthat):
    fuckthat = await fuckthat.client(getchat(fuckthat.chat_id))
    await fuckthat.client(getvc(fuckthat.full_chat.call, limit=1))
    return hehe.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@fanda_cmd(pattern="startvc$")
@register(pattern=r"^\.startvcs$", sudo=True)
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {ALIVE_NAME} Bukan Admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await edit_or_reply(c, "`Memulai Obrolan Suara`")
    except Exception as ex:
        await edit_or_reply(c, f"**ERROR:** `{ex}`")


@fanda_cmd(pattern="stopvc$")
@register(pattern=r"^\.stopvcs$", sudo=True)
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {ALIVE_NAME} Bukan Admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await edit_or_reply(c, "`Mematikan Obrolan Suara`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@fanda_cmd(pattern="vcinvite")
async def _(fanda):
    await edit_or_reply(fanda, "`Sedang Menginvite Member...`")
    users = []
    z = 0
    async for x in fanda.client.iter_participants(fanda.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await fanda.client(invitetovc(call=await get_call(fanda), users=p))
            z += 6
        except BaseException:
            pass
    await edit_or_reply(fanda, f"`Menginvite {z} Member`")


@fanda_cmd(pattern="vctitle(?: |$)(.*)")
@register(pattern=r"^\.cvctitle$", sudo=True)
async def change_title(e):
    title = e.pattern_match.group(1)
    me = await e.client.get_me()
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edit_delete(e, "**Silahkan Masukan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await edit_delete(e, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await edit_or_reply(e, f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edit_delete(e, f"**ERROR:** `{ex}`")


@fanda_cmd(pattern="joinvc(?: |$)(.*)", group_only=True)
@register(pattern=r"^\.joinvcs(?: |$)(.*)", sudo=True)
async def _(event):
    Onlyme = await edit_or_reply(event, "`Processing...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await Onlyme.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    if chat_id:
        file = "./userbot/resources/audio-ini.mp3"
        try:
            await call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await Onlyme.edit(
                f"• **Joined voice chat in:**\n`{chat_id}`"
            )
        except AlreadyJoinedError:
            return await edit_delete(
                Onlyme, "**INFO:** `akun anda sudah berada di obrolan suara`", 45
            )
        except Exception as e:
            return await Onlyme.edit(f"**INFO:** `{e}`")


@fanda_cmd(pattern="leavevc(?: |$)(.*)", group_only=True)
@register(pattern=r"^\.leavevcs(?: |$)(.*)", sudo=True)
async def vc_end(event):
    Onlyme = await edit_or_reply(event, "`Processing...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await Onlyme.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    if chat_id:
        try:
            await call_py.leave_group_call(chat_id)
            await edit_delete(
                Onlyme,
                f"• **Leave voice chat in:**\n`{chat_id}`",
            )
        except Exception as e:
            return await Onlyme.edit(f"**INFO:** `{e}`")


CMD_HELP.update(
    {
        "vctools": f"𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}startvc`\
         \n↳ : Memulai Obrolan Suara dalam Group.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}stopvc`\
         \n↳ : Menghentikan Obrolan Suara Pada Group.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}vctittle <tittle vcg>`\
         \n↳ : Mengubah tittle/judul Obrolan Suara.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}vcinvite`\
         \n↳ : Invite semua member yang berada di group.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}joinvc` or `{nothing}joinvc` <chatid/username gc>\
         \n↳ : Bergabung dengan obrolan suara grup.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{nothing}leavevc` or `{nothing}leavevc` <chatid/username gc>\
         \n↳ : Meninggalkan obrolan suara grup."
    }
)
