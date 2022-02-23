#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from utils import LOGGER
from pyrogram.types import Message
from config import Config
from pyrogram import (
    Client, 
    filters
)
from utils import (
    clear_db_playlist, 
    get_playlist_str, 
    is_admin, 
    mute, 
    restart_playout, 
    settings_panel, 
    skip, 
    pause, 
    resume, 
    unmute, 
    volume, 
    get_buttons, 
    is_admin, 
    seek_file, 
    delete_messages,
    chat_filter,
    volume_buttons
)

admin_filter=filters.create(is_admin)   

@Client.on_message(filters.command(["playlist", f"playlist@{Config.BOT_USERNAME}"]) & chat_filter)
async def player(client, message):
    if not Config.CALL_STATUS:
        await message.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([message])
        return
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            disable_web_page_preview=True,
            reply_markup=await get_buttons(),
        )
    else:
        if Config.msg.get('player') is not None:
            await Config.msg['player'].delete()
        Config.msg['player'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
            reply_markup=await get_buttons(),
        )
    await delete_messages([message])

@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def skip_track(_, m: Message):
    msg=await m.reply('incerc sa sar din lista de asteptare..')
    if not Config.CALL_STATUS:
        await msg.edit(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.playlist:
        await msg.edit("Playlist gasit gol momentan.")
        await delete_messages([m, msg])
        return
    if len(m.command) == 1:
        await skip()
    else:
        #https://github.com/callsmusic/tgvc-userbot/blob/dev/plugins/vc/player.py#L268-L288
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    await msg.edit(f"Eliminat cu succes din lista de redare- {i}. **{Config.playlist[i][1]}**")
                    await clear_db_playlist(song=Config.playlist[i])
                    Config.playlist.pop(i)
                    await delete_messages([m, msg])
                else:
                    await msg.edit(f"Nu poți sări peste primele două melodii- {i}")
                    await delete_messages([m, msg])
        except (ValueError, TypeError):
            await msg.edit("Intrare invalidă")
            await delete_messages([m, msg])
    pl=await get_playlist_str()
    if m.chat.type == "private":
        await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        if Config.msg.get('player'):
            await Config.msg['player'].delete()
        Config.msg['player'] = await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        await delete_messages([m])

@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def pause_playing(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if Config.PAUSE:
        k = await m.reply("Deja pus pe pauza")
        await delete_messages([m, k])
        return
    k = await m.reply("Apel video pus pe pauza")
    await pause()
    await delete_messages([m, k])
    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def resume_playing(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.PAUSE:
        k = await m.reply("Nimic nu s-a oprit pentru a relua")
        await delete_messages([m, k])
        return
    k = await m.reply("Apel video reluat")
    await resume()
    await delete_messages([m, k])
    


@Client.on_message(filters.command(['volume', f"volume@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if len(m.command) < 2:
        await m.reply_text('Schimbați volumul ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ', reply_markup=await volume_buttons())
        await delete_messages([m])
        return
    if not 1 < int(m.command[1]) < 200:
        await m.reply_text(f"Doar o valoare intre 1-200 este acceptata. ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", reply_markup=await volume_buttons())
    else:
        await volume(int(m.command[1]))
        await m.reply_text(f"Volum ajustat la {m.command[1]} ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", reply_markup=await volume_buttons())
    await delete_messages([m])

    


@Client.on_message(filters.command(['vcmute', f"vcmute@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_mute(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if Config.MUTED:
        k = await m.reply_text("Sunt deja pe mute.")
        await delete_messages([m, k])
        return
    k=await mute()
    if k:
        k = await m.reply_text(f" 🔇 Am fost pus pe mute ")
        await delete_messages([m, k])
    else:
        k = await m.reply_text("Sunt deja pus pe mute.")
        await delete_messages([m, k])
    
@Client.on_message(filters.command(['vcunmute', f"vcunmute@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def set_unmute(_, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    if not Config.MUTED:
        k = await m.reply("Streamul a fost scos de pe mute deja")
        await delete_messages([m, k])
        return
    k=await unmute()
    if k:
        k = await m.reply_text(f"🔊 Unmute ")
        await delete_messages([m, k])
        return
    else:
        k=await m.reply_text("Nu sunt pe mute, tocmai ce am fost scos.")    
        await delete_messages([m, k])


@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def replay_playout(client, m: Message):
    msg = await m.reply('Verific player')
    if not Config.CALL_STATUS:
        await msg.edit(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    await msg.edit(f"Replaying from begining")
    await restart_playout()
    await delete_messages([m, msg])


@Client.on_message(filters.command(["player", f"player@{Config.BOT_USERNAME}"]) & chat_filter)
async def show_player(client, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Player is idle, start the player using below button. ㅤㅤㅤㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    data=Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        title="<b>Acum redau Livestream</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    else:
        if Config.playlist:
            title=f"<b>{Config.playlist[0][1]}</b> ㅤㅤㅤㅤ\n ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        elif Config.STREAM_LINK:
            title=f"<b>Stream folosind [Url]({data['file']}) </b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        else:
            title=f"<b>Incepe streamul [stream]({Config.STREAM_URL})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    if m.chat.type == "private":
        await m.reply_text(
            title,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('player') is not None:
            await Config.msg['player'].delete()
        Config.msg['player'] = await m.reply_text(
            title,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])


@Client.on_message(filters.command(["seek", f"seek@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def seek_playout(client, m: Message):
    if not Config.CALL_STATUS:
        await m.reply_text(
            "Playerul este inactiv, porniți playerul folosind butonul de mai jos. ㅤㅤㅤ ㅤㅤ",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([m])
        return
    data=Config.DATA.get('FILE_DATA')
    k=await m.reply("Trying to seek..")
    if not data.get('dur', 0) or \
        data.get('dur') == 0:
        await k.edit("Acest stream nu poate fi derulat.")
        await delete_messages([m, k])
        return
    if ' ' in m.text:
        i, time = m.text.split(" ")
        try:
            time=int(time)
        except:
            await k.edit('Timp specificat invalid')
            await delete_messages([m, k])
            return
        nyav, string=await seek_file(time)
        if nyav == False:
            await k.edit(string)
            await delete_messages([m, k])
            return
        if not data.get('dur', 0)\
            or data.get('dur') == 0:
            title="<b>Acum redau Livestream</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        else:
            if Config.playlist:
                title=f"<b>{Config.playlist[0][1]}</b>\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
            elif Config.STREAM_LINK:
                title=f"<b>Stream folosind [Url]({data['file']})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
            else:
                title=f"<b>Incepe Streamul [stream]({Config.STREAM_URL})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        if Config.msg.get('player'):
            await Config.msg['player'].delete()  
        Config.msg['player'] = await k.edit(f"🎸{title}", reply_markup=await get_buttons(), disable_web_page_preview=True)
        await delete_messages([m])
    else:
        await k.edit('Nu a fost specificat un timp')
        await delete_messages([m, k])


@Client.on_message(filters.command(["settings", f"settings@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def settings(client, m: Message):
    await m.reply(f"Configurați setările VCPlayer aici. ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", reply_markup=await settings_panel(), disable_web_page_preview=True)
    await delete_messages([m])
