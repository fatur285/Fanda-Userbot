"""
This module updates the userbot based on upstream revision
"""

from os import remove, execle, path, environ
import asyncio
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HANDLER as shutup
from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_URL,
    UPSTREAM_REPO_BRANCH)
from userbot.utils import edit_or_reply, edit_delete, fanda_cmd

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        )
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await edit_or_reply(event,
                                "**[HEROKU]:** `Harap Siapkan Variabel` **HEROKU_APP_NAME** `"
                                " agar bisa memperbarui Fanda-Userbot.`"
                                )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await edit_delete(event,
                              f"{txt}\n`Kredensial Heroku tidak valid untuk deploy Fanda-Userbot dyno.`"
                              )
            return repo.__del__()
        await edit_or_reply(event,
                            "**[Heroku]:** `Sedang memperbarui 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁 mohon tunggu...`"
                            )
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
        except GitCommandError as error:
            await event.edit(f"{txt}\n`Terjadi Kesalahan Di Log:\n{error}`")
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await edit_delete(event,
                              "`Build Gagal!\n" "Dibatalkan atau ada beberapa kesalahan...`"
                              )
        else:
            await edit_delete(event,
                              "𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ **Berhasil di perbarui, Restarting tunggu sebentar...**"
                              )

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#UPDATER \n" "𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ Berhasil diperbarui."
            )

    else:
        await edit_delete(event,
                          "**[HEROKU]:**" "\n`Harap Siapkan Variabel` **HEROKU_API_KEY** `.`"
                          )
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    x = await edit_or_reply(event, "𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ Berhasil diperbarui.")
    await asyncio.sleep(2)
    await x.edit("'Sedang merestart....`")
    await asyncio.sleep(1)
    await x.edit("`Mohon tunggu beberapa detik.`")
    await asyncio.sleep(10)
    await x.delete()

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UPDATER \n" "𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ **Berhasil diperbarui.**"
        )
        await asyncio.sleep(100)
        await x.delete()

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@fanda_cmd(pattern="update(?: |$)(now|deploy)?")
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    xx = await edit_or_reply(event, "**Checking for updates...**")
    conf = event.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "`Mohon maaf, Pembaruan tidak dapat di lanjutkan karena "
        txt += "beberapa masalah terjadi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await xx.edit(f"{txt}\n`Directory {error} Tidak Dapat Di Temukan`")
        return repo.__del__()
    except GitCommandError as error:
        await xx.edit(f"{txt}\n`Gagal Awal! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await xx.edit(
                f"`Sayangnya, Directory {error} Tampaknya Bukan Dari Repo."
                "\nTapi Kita Bisa Memperbarui Paksa Userbot Menggunakan .update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await xx.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if changelog == "" and force_update is False:
        await xx.edit(
            f"\n𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ **Sudah Versi Terbaru Goblok! || Kunjungi @fandaproject untuk melihat berita terbaru tentang** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​.\n"
        )
        await asyncio.sleep(50)
        await xx.delete()
        return repo.__del__()

    if conf is None and force_update is False:
        changelog_str = (
            f"**Pembaruan Untuk** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​:\n\n⚒️ **Change log:**\n`{changelog}`"
        )
        if len(changelog_str) > 4096:
            await xx.edit("`Changelog Terlalu Besar, Lihat File Untuk Melihatnya.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await event.client.send_file(
                event.chat_id,
                "output.txt",
                reply_to=event.id,
            )
            remove("output.txt")
        else:
            await xx.edit(changelog_str)
        return await event.respond(
            f"**Perintah untuk memperbarui** 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​:\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update now`\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update deploy`"
        )

    if force_update:
        await xx.edit(
            "`Sinkronisasi Paksa Ke Kode Userbot Stabil Terbaru, Harap Tunggu .....`"
        )
    else:
        await xx.edit("`Mulai memperbarui 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​...`")
        await xx.edit("`Loading...0%`")
        await xx.edit("`Loading...5%`")
        await xx.edit("`Loading...10%`")
        await xx.edit("`Loading...15%`")
        await xx.edit("`Loading...20%`")
        await xx.edit("`Loading...25%`")
        await xx.edit("`Loading...30%`")
        await xx.edit("`Loading...35%`")
        await xx.edit("`Loading...40%`")
        await xx.edit("`Loading...45%`")
        await xx.edit("`Loading...50%`")
        await xx.edit("`Loading...55%`")
        await xx.edit("`Loading...60%`")
        await xx.edit("`Loading...65%`")
        await xx.edit("`Loading...70%`")
        await xx.edit("`Loading...75%`")
        await xx.edit("`Loading...80%`")
        await xx.edit("`Loading...85%`")
        await xx.edit("`Loading...90%`")
        await xx.edit("`Loading...95%`")
        await xx.edit("`Loading...100%`")
        await xx.edit("`Berhasil memperbarui 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​, Mohon tunggu sebentar...`"
        )

    if conf == "now":
        await update(event, repo, ups_rem, ac_br)
        await asyncio.sleep(10)
        await xx.delete()
    elif conf == "deploy":
        await deploy(event, repo, ups_rem, ac_br, txt)
        await asyncio.sleep(10)
        await xx.delete()
    return


CMD_HELP.update(
    {
        "update": f"𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update`"
        "\n• : Untuk Melihat Pembaruan dari 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​."
        f"\n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update now`"
        "\n• : Memperbarui 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​."
        f"\n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{shutup}update deploy`"
        "\n• : Memperbarui 𝗙𝗮𝗻𝗱𝗮-𝗨𝘀𝗲𝗿𝗯𝗼𝘁​ Dengan Cara Men-Deploy Ulang."
    }
)
