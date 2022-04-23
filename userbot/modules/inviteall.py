from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from userbot import OWNER, CMD_HELP, CMD_HANDLER as cmd
from userbot.events import register
from userbot.utils import edit_or_reply, fanda_cmd


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


@fanda_cmd(pattern="inviteall(?: |$)(.*)")
@register(incoming=True, from_users=OWNER,
          pattern=r"^\.cinvite(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        ohsi = await event.reply("`processing...`")
    else:
        ohsi = await edit_or_reply(event, "`processing...`")
    geezteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await ohsi.edit("`Sorry, Can add users here`")
    s = 0
    f = 0
    error = "None"

    await ohsi.edit("**TerminalStatus**\n\n`Collecting Users.......`")
    async for user in event.client.iter_participants(geezteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await ohsi.edit(
                    f"**Terminal Finished With Error**\n(`May Got Limit Error from telethon Please try agin Later`)\n**Error** : \n`{error}`\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people"
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await ohsi.edit(
                f"**Terminal Running...**\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await ohsi.edit(
        f"**Terminal Finished** \n\n• Successfully Invited `{s}` people \n• failed to invite `{f}` people"
    )


CMD_HELP.update(
    {
        "inviteall": f"𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{cmd}inviteall <@group username>`\
          \nUsage : Menambahkan pengguna grup lain ke dalam grup tempat perintah ini dijalankan."
    }
)
