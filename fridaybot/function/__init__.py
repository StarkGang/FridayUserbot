#    Copyright (C) Midhun KM 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import hachoir
import asyncio
import os
from pathlib import Path
import wget
from fridaybot.utils import load_module
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
import asyncio
import json
import math
import os
import re
import shlex
import subprocess
import time
import eyed3
from os.path import basename
from typing import List, Optional, Tuple
import webbrowser
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup as bs
import re
from telethon.tl.types import InputMessagesFilterDocument
import telethon
from telethon import Button, custom, events, functions
from pymediainfo import MediaInfo
from telethon.tl.types import MessageMediaPhoto
from typing import Union
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
BASE_URL = "https://isubtitles.org"
from fridaybot.Configs import Config
import zipfile
import os
import aiohttp
import cv2
import numpy as np
import dlib
import time
from fridaybot.function.FastTelethon import upload_file


sedpath = Config.TMP_DOWNLOAD_DIRECTORY
from fridaybot import logging

logger = logging.getLogger("[--WARNING--]")
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)
    
# Deethon // @aykxt
session = aiohttp.ClientSession()

async def fetch_json(link):
    async with session.get(link) as resp:
        return await resp.json()
    
    
def get_readable_file_size(size_in_bytes: Union[int, float]) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


def get_readable_time(secs: float) -> str:
    result = ""
    (days, remainder) = divmod(secs, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result
    
# Thanks To Userge-X
async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def extract_index_nparray(nparray):
    index = None
    for num in nparray[0]:
        index = num
        break
    return index

async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await event.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                    
                )
            except:
                pass
        else:
            try:
                await event.edit("{}\n{}".format(type_of_ps, tmp))
            except:
                pass
async def all_pro_s(Config, client2, client3, bot):
    if not Config.SUDO_USERS:
        lmao_s = []
    else:
        lmao_s = list(Config.SUDO_USERS)
    sed1 = await bot.get_me()
    lmao_s.append(sed1.id)
    if client2:
        sed2 = await client2.get_me()
        lmao_s.append(sed2.id)
    if client3:
        sed3 = await client3.get_me()
        lmao_s.append(sed3.id)
    return lmao_s

def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def get_all_modules(event, borg, channel_id):
    await event.edit(f"Ìnstalling All Plugins from {channel_id}")
    try:
        a_plugins = await borg.get_messages(
            entity=channel_id,
            filter=InputMessagesFilterDocument,
            limit=None,
            search=".py",
        )
    except:
        await event.edit("`Failed To Retrieve Modules. Please Check Channel Username / Id. Make Sure You Are On That Channel`")
        return
    yesm = 0
    nom = 0
    len_p = int(a_plugins.total)
    if len_p == 0:
        await event.edit("**No PLugins Found To Load !**")
        return
    await event.edit(f"**Found : {len_p} Plugins. Trying To Install**")
    for sed in a_plugins:
        try:
            downloaded_file_name = await borg.download_media(sed, "fridaybot/modules/")
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("**Installed :** `{}`".format(os.path.basename(downloaded_file_name)
                                                              )
                                )
            else:
                nom += 1
                await event.edit("**Failed to Install [PLugin Already Found] :** `{}`".format(os.path.basename(downloaded_file_name)
                                                              )
                                )
                os.remove(downloaded_file_name)
        except:
                await event.edit("**Failed To Install :** `{}`".format(os.path.basename(downloaded_file_name)
                                                              )
                                )
                os.remove(downloaded_file_name)
                nom += 1
                pass
    yesm = len_p - nom
    return yesm, nom, len_p

def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
            ((str(days) + " day(s), ") if days else "")
            + ((str(hours) + " hour(s), ") if hours else "")
            + ((str(minutes) + " minute(s), ") if minutes else "")
            + ((str(seconds) + " second(s), ") if seconds else "")
            + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


# Thanks To Userge-X
# Ported By @STARKXD
async def convert_to_image(event, borg):
    lmao = await event.get_reply_message()
    if not (
            lmao.gif
            or lmao.audio
            or lmao.voice
            or lmao.video
            or lmao.video_note
            or lmao.photo
            or lmao.sticker
            or lmao.media
    ):
        await event.edit("`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                lmao.media,
                sedpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.edit("Download Unsucessfull :(")
        return
    if lmao and lmao.photo:
        lmao_final = downloaded_file_name
    elif lmao.sticker and lmao.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(sedpath, "SED.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        lmao_final = image_name20
    elif lmao.sticker and lmao.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = sedpath + "image.png"
        os.rename(pathofsticker2, image_new_path)
        if not os.path.exists(image_new_path):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = image_new_path
    elif lmao.audio:
        sed_p = downloaded_file_name
        hmmyes = sedpath + "stark.mp3"
        imgpath = sedpath + "starky.jpg"
        os.rename(sed_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(sed_p)
        if not os.path.exists(imgpath):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = imgpath
    elif lmao.gif or lmao.video or lmao.video_note:
        sed_p2 = downloaded_file_name
        jpg_file = os.path.join(sedpath, "image.jpg")
        await take_screen_shot(sed_p2, 0, jpg_file)
        os.remove(sed_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Couldn't Fetch. SS`")
            return
        lmao_final = jpg_file
    await event.edit("`Almost Completed.`")
    return lmao_final


# Thanks To Userge-X
async def crop_vid(input_vid: str, final_path: str):
    media_info = MediaInfo.parse(input_vid)
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        os.system(f'ffmpeg -i {input_vid} -vf "crop={crop_by}:{crop_by}" {final_path}')
        os.remove(input_vid)
    else:
        os.rename(input_vid, final_path)


# Thanks To Userge-X
async def take_screen_shot(
        video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """ take a screenshot """
    logger.info(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join(sedpath, f"{basename(video_file)}.jpg")
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    if err:
        logger.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


# Thanks To @HeisenbergTheDanger, @xditya
async def fetch_feds(event, borg):
    fedList = []
    await event.edit("`Fetching Your FeD List`, This May Take A While.")
    reply_s = await event.get_reply_message()
    if reply_s and reply_s.media:
        downloaded_file_name = await borg.download_media(reply_s.media, "fedlist.txt")
        await asyncio.sleep(1)
        file = open(downloaded_file_name, "r")
        lines = file.readlines()
        for line in lines:
            try:
                fedList.append(line[:36])
            except:
                pass
                # CleanUp
        os.remove(downloaded_file_name)
        return fedList
    async with borg.conversation("@MissRose_bot") as bot_conv:
        await bot_conv.send_message("/start")
        await bot_conv.send_message("/myfeds")
        response = await bot_conv.get_response(timeout=300)
        if "You can only use fed commands once every 5 minutes" in response.text:
            await event.edit("`Try again after 5 mins.`")
            return
        elif "make a file" in response.text:
            await event.edit(
                "`Boss, You Real Peru. You Are Admin in So Many Feds. WoW!`"
            )
            await response.click(0)
            fedfile = await bot_conv.get_response()
            await asyncio.sleep(2)
            if "You can only use fed commands once every 5 minutes" in fedfile.text:
                await event.edit("`Try again after 5 mins.`")
                return
            if fedfile.media:
                downloaded_file_name = await borg.download_media(fedfile.media, "fedlist.txt")
                await asyncio.sleep(1)
                file = open(downloaded_file_name, "r")
                lines = file.readlines()
                for line in lines:
                    try:
                        fedList.append(line[:36])
                    except BaseException:
                        pass
                os.remove(downloaded_file_name)
        else:
            In = False
            tempFedId = ""
            for x in response.text:
                if x == "`":
                    if In:
                        In = False
                        fedList.append(tempFedId)
                        tempFedId = ""
                    else:
                        In = True

                elif In:
                    tempFedId += x
    await event.edit("`FeD List Fetched SucessFully.`")
    return fedList


async def get_imdb_id(search, event):
    link = "https://yts-subs.com/search/ajax?mov=" + search
    lol = requests.get(link)
    warner_bros = lol.json()
    if warner_bros == []:
        await event.edit("`No Results Found.`")
        warner_media = None
        warner_s = None
    else:
        warner_media = warner_bros[0]["mv_mainTitle"]
        warner_s = warner_bros[0]["mv_imdbCode"]
    return warner_media, warner_s


async def get_subtitles(imdb_id, borg, event):
    await event.edit("`Processing..`")
    link = f"https://yts-subs.com/movie-imdb/" + imdb_id
    movie_response = requests.get(url=link)
    subtitles = []
    soup1 = BeautifulSoup(movie_response.content, "html.parser")
    rows = soup1.find_all("tr", class_="high-rating")
    for row in rows:
        td = row.find("td", class_="flag-cell")
        lang = td.find("span", class_="sub-lang").text
        if lang == "English":
            sub_link_tag = row.find("td", class_="download-cell")
            sub_link = sub_link_tag.find("a", class_="subtitle-download").get("href")
            sub_link = f"https://yts-subs.com/{sub_link}"
            sub_name_tag = row.find("td", class_=None)
            sub_name = (
                str(sub_name_tag.find("a").text)
                    .replace("subtitle", "")
                    .replace("\n", "")
            )
            sub = (sub_name, sub_link)
            subtitles.append(sub)
    await event.edit("`Almost Done.`")
    sub_response = requests.get(url=subtitles[0]["sub_link"])
    selected_sub_name = subtitles[0]["sub_name"]
    soup2 = BeautifulSoup(sub_response.content, "html.parser")
    link = soup2.find("a", class_="btn-icon download-subtitle").get("href")
    final_response = requests.get(link, stream=True)
    await event.edit("`Downloading Now`")
    if final_response.status_code == 200:
        with open(sedpath + f"{selected_sub_name}.zip", "wb") as sfile:
            for byte in final_response.iter_content(chunk_size=128):
                sfile.write(byte)
    final_paths = sedpath + f"{selected_sub_name}.zip"
    namez = selected_sub_name
    return final_paths, namez, subtitles[0]["sub_link"]


# Thanks To TechoAryan For Scarpping
async def apk_dl(app_name, path, event):
    await event.edit('`Searching, For Apk File. This May Take Time Depending On Your App Size`')
    res = requests.get(f"https://m.apkpure.com/search?q={app_name}")
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.select('.dd')
    for link in result[:1]:
        s_for_name = requests.get("https://m.apkpure.com" + link.get('href'))
        sfn = BeautifulSoup(s_for_name.text, 'html.parser')
        ttl = sfn.select_one('title').text
        noneed = [' - APK Download']
        for i in noneed:
            name = ttl.replace(i, '')
            res2 = requests.get("https://m.apkpure.com" + link.get('href') + "/download?from=details")
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            result = soup2.select('.ga')
        for link in result:
            dl_link = link.get('href')
            r = requests.get(dl_link)
            with open(f"{path}/{name}@FridayOT.apk", 'wb') as f:
                f.write(r.content)
    await event.edit('`Apk, Downloaded. Let me Upload It here.`')
    final_path = f'{path}/{name}@FridayOT.apk'
    return final_path, name

async def check_if_subbed(channel_id, event, bot):
    try:
            result = await bot(
                functions.channels.GetParticipantRequest(
                    channel=channel_id, user_id=event.sender_id
                )
            )
            if result.participant:
                return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False
    
async def _ytdl(url, is_it, event, tgbot):
    await event.edit("`Ok Downloading This Video / Audio - Please Wait.` \n**Powered By @FridayOT**")
    if is_it:
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(title)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    else:
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(title)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except Exception as e:
        await event.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    if song:
        file_stark = f"{ytdl_data['title']}.mp3"
        lol_m = await upload_file(
            file_name=file_stark,
            client=tgbot,
            file=open(file_stark, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading Youtube Audio..", file_stark
                )
            ),
        )
        await event.edit(
            file=lol_m,
            text=f"{ytdl_data['title']} \n**Uploaded Using @FRidayOt**"
        )
        os.remove(file_stark)
    elif video:
        file_stark = f"{ytdl_data['title']}.mp4"
        lol_m = await upload_file(
            file_name=file_stark,
            client=tgbot,
            file=open(file_stark, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading Youtube Video..", file_stark
                )
            ),
        )
        await event.edit(
            file=lol_m,
            text=f"{ytdl_data['title']} \n**Uploaded Using @FRidayOt**"
        )
        os.remove(file_stark)


async def _deezer_dl(word, event, tgbot):
    await event.edit("`Ok Downloading This Audio - Please Wait.` \n**Powered By @FridayOT**")
    urlp = f"https://starkapi.herokuapp.com/deezer/{word}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    mello = datto.get("artist")
    #thums = urlhp["album"]["cover_medium"]
    sname = f'''{datto.get("title")}.mp3'''
    doc = requests.get(mus)
    with open(sname, 'wb') as f:
      f.write(doc.content)
    car = f"""
**Song Name :** {datto.get("title")}
**Duration :** {datto.get('duration')} Seconds
**Artist :** {mello}

Music Downloaded And Uploaded By Friday Userbot

Get Your Friday From @FridayOT"""
    await event.edit("Song Downloaded.  Waiting To Upload. 🥳🤗")
    c_time = time.time()
    uploaded_file = await upload_file(
        	file_name=sname,
            client=tgbot,
            file=open(sname, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading..", sname
                )
            ),
        )
    
    await event.edit(
            file=uploaded_file,
            text=car
    )
    os.remove(sname)




                  
async def get_all_admin_chats(event):
    lul_stark = []
    all_chats = [
        d.entity
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
    for i in all_chats:
        if i.creator or i.admin_rights:
            lul_stark.append(i.id)
    return lul_stark

                  
async def is_admin(event, user):
    sed = await event.client.get_permissions(event.chat_id, user)
    if sed.is_admin:
        is_mod = True
    else:
        is_mod = False
    return is_mod
                  
                  
