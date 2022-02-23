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
from contextlib import suppress
from config import Config
import calendar
import pytz
from datetime import datetime
import asyncio
import os
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, 
    MessageNotModified
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from utils import (
    cancel_all_schedules,
    edit_config, 
    is_admin, 
    leave_call, 
    restart,
    restart_playout,
    stop_recording, 
    sync_to_db,
    update, 
    is_admin, 
    chat_filter,
    sudo_filter,
    delete_messages,
    seek_file
)
from pyrogram import (
    Client, 
    filters
)

IST = pytz.timezone(Config.TIME_ZONE)
if Config.DATABASE_URI:
    from utils import db

HOME_TEXT = "<b>Salut/Buna  [{}](tg://user?id={}) 🐺♂️\n\nSunt un BOT creat sa redau videoclipuri sau streamuri in canalele de voce pe telegram.\nPot sa redau orice videoclip de pe YouTube sau video trimis in chat pe telegram, chiar si live de YouTube.</b>"
admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if len(message.command) > 1:
        if message.command[1] == 'help':
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"Play", callback_data='help_play'),
                        InlineKeyboardButton(f"Setari", callback_data=f"help_settings"),
                        InlineKeyboardButton(f"Inregistrare", callback_data='help_record'),
                    ],
                    [
                        InlineKeyboardButton("Programare", callback_data="help_schedule"),
                        InlineKeyboardButton("Controale", callback_data='help_control'),
                        InlineKeyboardButton("Admini", callback_data="help_admin"),
                    ],
                    [
                        InlineKeyboardButton(f"Altele", callback_data='help_misc'),
                        InlineKeyboardButton("Inchide", callback_data="close"),
                    ],
                ]
                )
            await message.reply("Învață să folosești VCPlayer, Arat meniul de ajutor, Alege dintre opțiunile de mai jos.",
                reply_markup=reply_markup,
                disable_web_page_preview=True
                )
        elif 'sch' in message.command[1]:
            msg=await message.reply("Verific programari..")
            you, me = message.command[1].split("_", 1)
            who=Config.SCHEDULED_STREAM.get(me)
            if not who:
                return await msg.edit("Ceva s-a dus undeva.")
            del Config.SCHEDULED_STREAM[me]
            whom=f"{message.chat.id}_{msg.message_id}"
            Config.SCHEDULED_STREAM[whom] = who
            await sync_to_db()
            if message.from_user.id not in Config.ADMINS:
                return await msg.edit("OK da")
            today = datetime.now(IST)
            smonth=today.strftime("%B")
            obj = calendar.Calendar()
            thisday = today.day
            year = today.year
            month = today.month
            m=obj.monthdayscalendar(year, month)
            button=[]
            button.append([InlineKeyboardButton(text=f"{str(smonth)}  {str(year)}",callback_data=f"sch_month_choose_none_none")])
            days=["Lun", "Mar", "Mie", "Joi", "Vin", "Sam", "Dum"]
            f=[]
            for day in days:
                f.append(InlineKeyboardButton(text=f"{day}",callback_data=f"day_info_none"))
            button.append(f)
            for one in m:
                f=[]
                for d in one:
                    year_=year
                    if d < int(today.day):
                        year_ += 1
                    if d == 0:
                        k="\u2063"   
                        d="none"   
                    else:
                        k=d    
                    f.append(InlineKeyboardButton(text=f"{k}",callback_data=f"sch_month_{year_}_{month}_{d}"))
                button.append(f)
            button.append([InlineKeyboardButton("Inchide", callback_data="schclose")])
            await msg.edit(f"Alegeți ziua din lună în care doriți să programați conversația vocală.\Astăzi este {thisday} {smonth} {year}. Chooosing a date preceeding today will be considered as next year {year+1}", reply_markup=InlineKeyboardMarkup(button))



        return
    buttons = [
        [
            InlineKeyboardButton('🇷🇴 Portal ❌ OTR 🇦🇱', url='https://t.me/OTRportal'),
            InlineKeyboardButton('H.A.I.T.A.🐺🎭😍⚔❤', url='https://t.me/LupiiDinHaita')
        ],
        [
            InlineKeyboardButton('👨🏼‍🦯 Ajutor', callback_data='help_main'),
            InlineKeyboardButton('🗑 Inchide', callback_data='close'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    k = await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await delete_messages([message, k])



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Play", callback_data='help_play'),
                InlineKeyboardButton("Setari", callback_data=f"help_settings"),
                InlineKeyboardButton("Inregistrare", callback_data='help_record'),
            ],
            [
                InlineKeyboardButton("Programare", callback_data="help_schedule"),
                InlineKeyboardButton("Controale", callback_data='help_control'),
                InlineKeyboardButton("Admini", callback_data="help_admin"),
            ],
            [
                InlineKeyboardButton("Altele", callback_data='help_misc'),
                InlineKeyboardButton("Config ENV", callback_data='help_env'),
                InlineKeyboardButton("Inchide", callback_data="close"),
            ],
        ]
        )
    if message.chat.type != "private" and message.from_user is None:
        k=await message.reply(
            text="Nu te pot ajuta aici, deoarece ești un administrator anonim. Obțineți ajutor în PM",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"Ajutor", url=f"https://telegram.dog/{Config.BOT_USERNAME}?start=help"),
                    ]
                ]
            ),)
        await delete_messages([message, k])
        return
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        "Învață să folosești VCPlayer, Arat meniul de ajutor, Alege dintre opțiunile de mai jos.",
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
    #await delete_messages([message])
@Client.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton('🇷🇴 Portal ❌ OTR 🇦🇱', url='https://t.me/OTRportal'),
            InlineKeyboardButton('H.A.I.T.A.🐺🎭😍⚔❤', url='https://t.me/LupiiDinHaita') 
        ],
        [
            InlineKeyboardButton("🎞 How to Deploy", url='https://youtu.be/dQw4w9WgXcQ'),
            InlineKeyboardButton('🗑 Inchide', callback_data='close'),
        ]
    ]
    await message.reply("<b>Codul sursă al acestui bot este public și poate fi găsit la <a href=https://t.me/LupiiDinHaita>VCPlayerBot.</a>\nÎți poți implementa propriul bot și îl poți folosi în grupul tău.\n\nDaca iti da voie @werwolf96 🙃.</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await delete_messages([message])

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k = await message.reply("Aplicația Heroku a fost găsită, se repornește botu pentru actualizare.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
            await sync_to_db()
    else:
        k = await message.reply("Aplicația Heroku a fost găsită, Încerc să repornesc.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
    try:
        await message.delete()
    except:
        pass
    await update()

@Client.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def get_logs(client, message):
    m=await message.reply("Verific logu..")
    if os.path.exists("botlog.txt"):
        await message.reply_document('botlog.txt', caption="Bot Logs")
        await m.delete()
        await delete_messages([message])
    else:
        k = await m.edit("No log files found.")
        await delete_messages([message, k])

@Client.on_message(filters.command(['env', f"env@{Config.BOT_USERNAME}", "config", f"config@{Config.BOT_USERNAME}"]) & sudo_filter & chat_filter)
async def set_heroku_var(client, message):
    with suppress(MessageIdInvalid, MessageNotModified):
        m = await message.reply("Checking config vars..")
        if " " in message.text:
            cmd, env = message.text.split(" ", 1)
            if "=" in env:
                var, value = env.split("=", 1)
            else:
                if env == "STARTUP_STREAM":
                    env_ = "STREAM_URL"
                elif env == "QUALITY":
                    env_ = "CUSTOM_QUALITY" 
                else:
                    env_ = env
                ENV_VARS = ["ADMINS", "SUDO", "CHAT", "LOG_GROUP", "STREAM_URL", "SHUFFLE", "ADMIN_ONLY", "REPLY_MESSAGE", 
                        "EDIT_TITLE", "RECORDING_DUMP", "RECORDING_TITLE", "IS_VIDEO", "IS_LOOP", "DELAY", "PORTRAIT", 
                        "IS_VIDEO_RECORD", "PTN", "CUSTOM_QUALITY"]
                if env_ in ENV_VARS:
                    await m.edit(f"Valoarea curentă pentru `{env}`  este `{getattr(Config, env_)}`")
                    await delete_messages([message])
                    return
                else:
                    await m.edit("Aceasta este o valoare nevalidă. Citiți ajutorul despre env pentru a afla despre valorile de env disponibile.")
                    await delete_messages([message, m])
                    return     
            
        else:
            await m.edit("Nu ați furnizat nicio valoare pentru env, ar trebui să urmați formatul corect.\nExemplu: <code>/env CHAT=-1020202020202</code> pentru a schimba sau a seta CHATU env.\n<code>/env REPLY_MESSAGE= <code>Pentru a sterge REPLY_MESSAGE.")
            await delete_messages([message, m])
            return

        if Config.DATABASE_URI and var in ["STARTUP_STREAM", "CHAT", "LOG_GROUP", "REPLY_MESSAGE", "DELAY", "RECORDING_DUMP", "QUALITY"]:      
            await m.edit("Mongo DB Gasit, Setez config vars...")
            await asyncio.sleep(2)  
            if not value:
                await m.edit(f"Nu a fost specificată nicio valoare pentru env. Se încearcă ștergerea env {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY"]:
                    await m.edit("Acesta este un var obligatoriu și nu poate fi șters.")
                    await delete_messages([message, m]) 
                    return
                await edit_config(var, False)
                await m.edit(f"Sucessfully deleted {var}")
                await delete_messages([message, m])           
                return
            else:
                if var in ["CHAT", "LOG_GROUP", "RECORDING_DUMP", "QUALITY"]:
                    try:
                        value=int(value)
                    except:
                        if var == "QUALITY":
                            if not value.lower() in ["low", "medium", "high"]:
                                await m.edit("Ar trebui să specificați o valoare între 10 - 100.")
                                await delete_messages([message, m])
                                return
                            else:
                                value = value.lower()
                                if value == "high":
                                    value = 100
                                elif value == "medium":
                                    value = 66.9
                                elif value == "low":
                                    value = 50
                        else:
                            await m.edit("Ar trebui sa imi dai un CHAT ID.")
                            await delete_messages([message, m])
                            return
                    if var == "CHAT":
                        await leave_call()
                        Config.ADMIN_CACHE=False
                        if Config.IS_RECORDING:
                            await stop_recording()
                        await cancel_all_schedules()
                        Config.CHAT=int(value)
                        await restart()
                    await edit_config(var, int(value))
                    if var == "QUALITY":
                        if Config.CALL_STATUS:
                            data=Config.DATA.get('FILE_DATA')
                            if not data \
                                or data.get('dur', 0) == 0:
                                await restart_playout()
                                return
                            k, reply = await seek_file(0)
                            if k == False:
                                await restart_playout()
                    await m.edit(f"Succesfully changed {var} to {value}")
                    await delete_messages([message, m])
                    return
                else:
                    if var == "STARTUP_STREAM":
                        Config.STREAM_SETUP=False
                    await edit_config(var, value)
                    await m.edit(f"S-a schimbat cu succes {var} in {value}")
                    await delete_messages([message, m])
                    await restart_playout()
                    return
        else:
            if not Config.HEROKU_APP:
                buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('🗑 Close', callback_data='close'),]]
                await m.edit(
                    text="Nu a fost găsită nicio aplicație Heroku, această comandă necesită setarea următoarelor variante Heroku.\n\n1. <code>HEROKU_API_KEY</code>: Your heroku account api key.\n2. <code>HEROKU_APP_NAME</code>: Your heroku app name.", 
                    reply_markup=InlineKeyboardMarkup(buttons)) 
                await delete_messages([message])
                return     
            config = Config.HEROKU_APP.config()
            if not value:
                await m.edit(f"Nu a fost specificată nicio valoare pentru env. Se încearcă ștergerea env {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY", "API_ID", "API_HASH", "BOT_TOKEN", "SESSION_STRING", "ADMINS"]:
                    await m.edit("Acestea sunt variante obligatorii și nu pot fi șterse.")
                    await delete_messages([message, m])
                    return
                if var in config:
                    await m.edit(f"S-a șters cu succes {var}")
                    await asyncio.sleep(2)
                    await m.edit("Acum reporniți aplicația pentru a face modificări.")
                    if Config.DATABASE_URI:
                        msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                        if not await db.is_saved("RESTART"):
                            db.add_config("RESTART", msg)
                        else:
                            await db.edit_config("RESTART", msg)
                    del config[var]                
                    config[var] = None               
                else:
                    k = await m.edit(f"Niciun mediu numit {var} găsit. Nu s-a schimbat nimic.")
                    await delete_messages([message, k])
                return
            if var in config:
                await m.edit(f"Variabilă deja găsită. Acum editat la {value}")
            else:
                await m.edit(f"Variabila nu a fost găsită, acum se setează ca var.")
            await asyncio.sleep(2)
            await m.edit(f"Setat cu succes {var} cu valoare {value}, Acum se repornește pentru a intra în vigoare modificările...")
            if Config.DATABASE_URI:
                msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                if not await db.is_saved("RESTART"):
                    db.add_config("RESTART", msg)
                else:
                    await db.edit_config("RESTART", msg)
            config[var] = str(value)




