"""
This module updates the userbot based on upstream revision
"""

import sys
from base64 import b64decode
from os import environ, execle, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HANDLER as shutup
from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply, fanda_cmd


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"• [{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(xx, ac_br, changelog):
    changelog_str = (
        f"**Pembaruan** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​:\n\n⚒️ **Change log:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await edit_or_reply(xx, "**Changelog terlalu besar, dikirim sebagai file.**")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await xx.client.send_file(xx.chat_id, "output.txt")
        remove("output.txt")
    else:
        await xx.client.send_message(xx.chat_id, changelog_str)
    return True


async def deploy(xx, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await edit_or_reply(
                xx,
                "**[HEROKU]: Harap Tambahkan Variabel** `HEROKU_APP_NAME` "
                " **untuk deploy perubahan terbaru dari Userbot.**",
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await edit_or_reply(
                xx,
                f"{txt}\n"
                "**Kredensial Heroku tidak valid untuk deploy Man-Userbot dyno.**",
            )
            return repo.__del__()
        try:
            from userbot.modules.sql_helper.globals import addgvar, delgvar

            delgvar("restartstatus")
            addgvar("restartstatus", f"{xx.chat_id}\n{xx.id}")
        except AttributeError:
            pass
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await edit_or_reply(xx, f"{txt}\n**Terjadi Kesalahan Di Log:**\n`{error}`")
            return repo.__del__()
        build = heroku_app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await edit_delete(
                xx, "**Build Gagal!** Dibatalkan karena ada beberapa error.`"
            )
        await edit_or_reply(
            xx, "`𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁 Berhasil Di Deploy! Userbot bisa di gunakan kembali.`"
        )

    else:
        return await edit_delete(
            xx, "**[HEROKU]: Harap Tambahkan Variabel** `HEROKU_API_KEY`"
        )


async def update(xx, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await edit_or_reply(
        xx, "`𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁 Berhasil diperbarui! Userbot dapat digunakan kembali.`"
    )

    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{xx.chat_id}\n{xx.id}")
    except AttributeError:
        pass

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@fanda_cmd(pattern="update( now| deploy|$)")
@register(pattern=r"^\.cupdate( now| deploy|$)", sudo=True)
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    xx = await edit_or_reply(event, "`Checking for update, Plis wait...`")
    conf = event.pattern_match.group(1).strip()
    off_repo = b64decode(
        "aHR0cHM6Ly9naXRodWIuY29tL0RJT1JyaW9zMjg1L0ZhbmRhLVVzZXJib3Q="
    ).decode("utf-8")
    force_update = False
    try:
        txt = (
            "**Pembaruan tidak dapat di lanjutkan karena "
            + "terjadi beberapa ERROR**\n\n**LOGTRACE:**\n"
        )
        repo = Repo()
    except NoSuchPathError as error:
        await xx.edit(f"{txt}\n**Directory** `{error}` **Tidak dapat di temukan.**")
        return repo.__del__()
    except GitCommandError as error:
        await xx.edit(f"{txt}\n**Kegagalan awal!** `{error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await xx.edit(
                f"**Sayangnya, Directory {error} Tampaknya Bukan Dari Repo. Tapi Kita Bisa Memperbarui Paksa Userbot Menggunakan** `{shutup}update deploy`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if conf == "deploy":
        await xx.edit("`[HEROKU]: Update deploy 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁 sedang dalam proses...`")
        await deploy(xx, repo, ups_rem, ac_br, txt)
        return

    if changelog == "" and not force_update:
        await edit_delete(xx, "𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ **Sudah Versi Terbaru Goblok! || Kunjungi** @fandaproject **untuk melihat berita terbaru tentang** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​.")
        return repo.__del__()

    if conf == "" and not force_update:
        await print_changelogs(xx, ac_br, changelog)
        await xx.delete()
        return await event.respond(
            f"**Perintah untuk memperbarui** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​:\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update deploy`"
        )

    if force_update:
        await xx.edit("**Sinkronisasi Paksa Ke Kode Userbot Terbaru, Harap Tunggu...**")

    if conf == "now":
        for commit in changelog.splitlines():
            if (
                commit.startswith("- [NQ]")
                and HEROKU_APP_NAME is not None
                and HEROKU_API_KEY is not None
            ):
                return await xx.edit(
                    f"**Quick update telah dinonaktifkan untuk pembaruan ini Gunakan** `{shutup}update deploy` **sebagai gantinya.**"
                )
        await xx.edit("**Perfoming a quick update, please wait...**")
        await update(xx, repo, ups_rem, ac_br)

    return


CMD_HELP.update(
    {
        "update": f"**Plugin : **`update`\
        \n\n  •  **Syntax :** `{shutup}update`\
        \n  •  **Function : **Untuk Melihat Pembaruan Terbaru 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁.\
        \n\n  •  **Syntax :** `{shutup}update deploy`\
        \n  •  **Function : **Untuk memperbarui fitur terbaru dari 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁.\
    "
    }
)
