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
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", "")
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "Cluster0")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", "")
    APP_NAME=os.environ.get("HEROKU_APP_NAME", "")


    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "False"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'True'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'True'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))
    PTN=is_enabled(os.environ.get("PTN", "False"))

    #Quality vars
    E_BITRATE=os.environ.get("BITRATE", False)
    E_FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "100")

    #Search filters for cplay
    FILTERS =  [filter.lower() for filter in (os.environ.get("FILTERS", "video document")).split(" ")]


    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]
    CONFIG_LIST = ["ADMINS", "IS_VIDEO", "IS_LOOP", "REPLY_PM", "ADMIN_ONLY", "SHUFFLE", "EDIT_TITLE", "CHAT", 
    "SUDO", "REPLY_MESSAGE", "STREAM_URL", "DELAY", "LOG_GROUP", "SCHEDULED_STREAM", "SCHEDULE_LIST", 
    "IS_VIDEO_RECORD", "IS_RECORDING", "WAS_RECORDING", "RECORDING_TITLE", "PORTRAIT", "RECORDING_DUMP", "HAS_SCHEDULE", 
    "CUSTOM_QUALITY"]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    CPLAY=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=100
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=True
        LOGGER.info("Reply Message Found, Enabled PM MSG")
    else:
        REPLY_MESSAGE=False
        REPLY_PM=False

    if E_BITRATE:
       try:
          BITRATE=int(E_BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          E_BITRATE=False
          BITRATE=48000
       if not BITRATE >= 48000:
          BITRATE=48000
    else:
       BITRATE=48000
    
    if E_FPS:
       try:
          FPS=int(E_FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          E_FPS=False
       if not FPS >= 50:
          FPS=50
    else:
       FPS=50
    try:
       CUSTOM_QUALITY=int(CUSTOM_QUALITY)
       if CUSTOM_QUALITY > 100:
          CUSTOM_QUALITY = 100
          LOGGER.warning("maximum quality allowed is 100, invalid quality specified. Quality set to 100")
       elif CUSTOM_QUALITY < 10:
          LOGGER.warning("Minimum Quality allowed is 10., Qulaity set to 10")
          CUSTOM_QUALITY = 10
       if  66.9  < CUSTOM_QUALITY < 100:
          if not E_BITRATE:
             BITRATE=48000
       elif 50 < CUSTOM_QUALITY < 66.9:
          if not E_BITRATE:
             BITRATE=36000
       else:
          if not E_BITRATE:
             BITRATE=24000
    except:
       if CUSTOM_QUALITY.lower() == 'high':
          CUSTOM_QUALITY=100
       elif CUSTOM_QUALITY.lower() == 'medium':
          CUSTOM_QUALITY=66.9
       elif CUSTOM_QUALITY.lower() == 'low':
          CUSTOM_QUALITY=50
       else:
          LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
          CUSTOM_QUALITY=100



    #help strings 
    PLAY_HELP="""
__Pute??i reda folosind oricare dintre aceste op??iuni__

1. Reda??i un videoclip de la un link YouTube.
Comanda: **/play**
__Pute??i folosi acest lucru ca r??spuns la un link YouTube sau transmite??i link-ul ??mpreun?? cu o comand??. sau ca r??spuns la mesaj pentru a c??uta pe YouTube.__

2. Reda??i dintr-un fi??ier telegram.
Comanda: **/play**
__R??spunde??i la un suport media acceptat (video ??i documente sau fi??ier audio).__
Not??: __Pentru ambele cazuri, /fplay poate fi folosit ??i de administratori pentru a reda melodia imediat, f??r?? a a??tepta s?? se termine coada.__

3. Reda??i dintr-o list?? de redare YouTube
Comanda: **/yplay**
__Mai ??nt??i ob??ine??i un fi??ier de playlist de la @GetPlaylistBot sau @DumpPlaylist ??i r??spunde??i la fi??ierul de playlist.__

4. Live Stream
Comanda: **/stream**
__Trimite??i o adres?? URL a streamului live sau orice adres?? URL direct?? pentru a-l reda ca stream.__

5. Importa??i o list?? de redare veche.
Comanda: **/import**
__R??spunde??i la un fi??ier de list?? de redare exportat anterior. __

6. Redare canal
Comanda: **/cplay**
__Utiliza??i `/cplay nume de utilizator al canalului sau id-ul canalului` pentru a reda toate fi??ierele de pe canalul dat.
??n mod implicit, vor fi redate at??t fi??ierele video, c??t ??i documentele. Pute??i ad??uga sau elimina tipul de fi??ier folosind `FILTER` var.
De exemplu, pentru a transmite ??n stream audio, video ??i documente de pe canal, utiliza??i `/env FILTERS video document audio` . Dac?? ave??i nevoie doar de audio, pute??i utiliza `/env FILTERS video audio` ??i a??a mai departe.
Pentru a configura fi??ierele de pe un canal ca STARTUP_STREAM, astfel ??nc??t fi??ierele s?? fie ad??ugate automat la lista de redare la pornirea botului. utiliza??i `/env STARTUP_STREAM nume de utilizator al canalului sau id-ul canalului`

Re??ine??i c?? pentru canalele publice ar trebui s?? utiliza??i numele de utilizator al canalelor ??mpreun?? cu ???@???, iar pentru canalele private ar trebui s?? utiliza??i ID-ul canalului.
Pentru canalele private, asigura??i-v?? c?? at??t botul, c??t ??i contul USER sunt membri ai canalului.__
"""
    SETTINGS_HELP="""
** V?? pute??i personaliza cu u??urin???? playerul ??n func??ie de nevoi. Sunt disponibile urm??toarele configura??ii:**

????Comand??: **/settings**

????CONFIGURA??II DISPONIBILE:

**Modul Player** - __Acest lucru v?? permite s?? rula??i playerul ca player muzical 24/7 sau numai atunci c??nd exist?? o melodie ??n coad??.
Dac?? este dezactivat, playerul va p??r??si apelul c??nd lista de redare este goal??.
??n caz contrar, STARTUP_STREAM va fi transmis ??n stream c??nd id-ul listei de redare este gol.__

**Video Enabled** - __Acest lucru v?? permite s?? comuta??i ??ntre audio ??i video.
dac?? este dezactivat, fi??ierele video vor fi redate ca audio.__

**Numai administrator** - __Activarea acestei op??iuni va restric??iona utilizatorii care nu sunt administratori s?? foloseasc?? comanda de redare.__

**Editeaz?? titlul** - __Activ??nd aceast?? op??iune, se va edita titlul VideoChat-ului la numele melodiilor ??n curs de redare.__

**Mod aleatoriu** - __Activarea acestui lucru va amesteca lista de redare ori de c??te ori importa??i o list?? de redare sau utiliza??i /yplay __

**R??spuns automat** - __Alege??i dac?? dori??i s?? r??spunde??i la mesajele PM ale contului de utilizator ??n redare.
Pute??i configura un mesaj de r??spuns personalizat folosind `REPLY_MESSAGE` confug.__

"""
    SCHEDULER_HELP="""
__VCPlayer v?? permite s?? programa??i un stream.
Aceasta ??nseamn?? c?? pute??i programa un stream pentru o dat?? viitoare, iar la data programat??, streamul va fi redat automat.
??n prezent pute??i programa un stream chiar ??i pentru un an!!. Asigura??i-v?? c?? a??i configurat o baz?? de date, altfel v?? ve??i pierde programele de fiecare dat?? c??nd playerul reporne??te. __

Comanda: **/schedule**

__R??spunde??i la un fi??ier sau un videoclip de pe youtube sau chiar la un mesaj text cu comanda de programare.
Media cu r??spuns sau videoclipul de pe youtube va fi programat ??i va fi redat la data programat??.
Ora de programare este implicit ??n IST ??i pute??i schimba fusul orar folosind configura??ia `TIME_ZONE`.__

Comanda: **/slist**
__Vizualiza??i streamurile dvs. programate curente.__

Comanda: **/cancel**
__Anula??i un program dup?? id-ul s??u de program, pute??i ob??ine ID-ul programului folosind comanda /slist__

Comanda: **/cancelall**
__Anuleaz?? toate streamurile programate__
"""
    RECORDER_HELP="""
__Cu VCPlayer v?? pute??i ??nregistra cu u??urin???? toate conversa??iile video.
??n mod implicit, telegram v?? permite s?? ??nregistra??i pentru o durat?? maxim?? de 4 ore.
O ??ncercare de a dep????i aceast?? limit?? a fost f??cut?? prin repornirea automat?? a ??nregistr??rii dup?? 4 ore__

Comanda: **/record**

CONFIGURA??II DISPONIBILE:
1. ??nregistrare video: __Dac?? este activat, at??t videoclipul, c??t ??i sunetul streamului vor fi ??nregistrate, altfel doar audio va fi ??nregistrat.__

2. Dimensiunea video: __Alege??i ??ntre dimensiunile portret ??i peisaj pentru ??nregistrarea dvs.__

3. Titlu de ??nregistrare personalizat: __Configura??i un titlu de ??nregistrare personalizat pentru ??nregistr??rile dvs. Utiliza??i o comand?? /rtitle pentru a configura acest lucru.
Pentru a dezactiva titlul personalizat, utiliza??i `/rtitle False `__

4. ??nregistrare stupid??: __Pute??i configura redirec??ionarea tuturor ??nregistr??rilor dvs. c??tre un canal, acest lucru va fi util deoarece, altfel, ??nregistr??rile sunt trimise c??tre mesajele salvate din contul de streaming.
Configura??i folosind configura??ia `RECORDING_DUMP`.__

?????? Dac?? ??ncepe??i o ??nregistrare cu vcplayer, asigura??i-v?? c?? opri??i acela??i lucru cu vcplayer.

"""

    CONTROL_HELP="""
__VCPlayer v?? permite s?? v?? controla??i streamurile cu u??urin????__
1. Sari peste o melodie.
Comanda: **/skip**
__Pute??i trece un num??r mai mare de 2 pentru a s??ri peste melodia ??n acea pozi??ie.__

2. ??ntrerupe??i playerul.
Comanda: **/pauz??**

3. Relua??i playerul.
Comanda: **/reluare**

4. Schimba??i volumul.
Comanda: **/volum**
__Trece??i volumul ??ntre 1-200.__

5. P??r??si??i VC.
Comanda: **/leave**

6. Amesteca??i lista de redare.
Comanda: **/shuffle**

7. ??terge??i lista curent?? de redare.
Comanda: **/clearplaylist**

8. C??uta??i videoclipul.
Comanda: **/seek**
__Pute??i trece un num??r de secunde pentru a fi s??rit. Exemplu: /seek 10 pentru a s??ri peste 10 sec. /seek -10 pentru a derula ??napoi 10 sec.__

9. Dezactiva??i sunetul playerului.
Comanda: **/vcmute**

10. Activa??i sunetul playerului.
Comanda: **/vcunmute**

11. Afi??eaz?? lista de redare.
Comanda: **/playlist**
__Folosi??i /player pentru a afi??a cu butoanele de control__
"""

    ADMIN_HELP="""
__VCPlayer v?? permite s?? controla??i administratorii, adic?? pute??i ad??uga administratori ??i ??i pute??i elimina cu u??urin????.
Este recomandat s?? utiliza??i o baz?? de date MongoDb pentru o experien???? mai bun??, altfel to??i administratorii dvs. vor fi resetati dup?? repornire.__

Comanda: **/vcpromote**
__Pute??i promova un administrator cu numele de utilizator sau id-ul de utilizator sau r??spunz??nd la mesajul respectiv.__

Comanda: **/vcdemote**
__Elimina??i un administrator din lista de administratori__

Comanda: **/refresh**
__Actualiza??i lista de administratori a chat__
"""

    MISC_HELP="""
Comanda: **/export**
__VCPlayer v?? permite s?? exporta??i lista de redare curent?? pentru o utilizare viitoare.__
__V?? fi trimis un fi??ier json ??i acela??i lucru poate fi folosit ??mpreun?? cu comanda /import.__

Comanda: **/logs**
__Dac?? playerul dvs. a mers prost, pute??i verifica cu u??urin???? jurnalele folosind /logs__
 
Comanda: **/env**
__Configura??i config vars cu comanda /env.__
__Exemplu: pentru a configura un__ `REPLY_MESSAGE` __use__ `/env REPLY_MESSAGE=Hei, verifica??i @subin_works ??n loc s?? trimite??i spam ??n PM`__
__Pute??i ??terge o config var omit??nd o valoare pentru aceasta, Exemplu:__ `/env LOG_GROUP=` __acest lucru va ??terge configura??ia existent?? LOG_GROUP.

Comanda: **/config**
__La fel cu utilizarea /env**

Comanda: **/update**
__Actualizeaz?? dvs. bot cu cele mai recente modific??ri__

Sfat: __Pute??i schimba cu u??urin???? configura??ia CHAT ad??ug??nd contul de utilizator ??i contul bot la orice alt grup ??i orice comand?? din grupul nou__

"""
    ENV_HELP="""
**Acestea sunt variantele configurabile disponibile ??i le pute??i seta pe fiecare folosind comanda /env**


**Vars obligatorii**

1. `API_ID`: __Get From [my.telegram.org](https://my.telegram.org/)__

2. `API_HASH` : __Ob??ine??i de la [my.telegram.org](https://my.telegram.org)__

3. `BOT_TOKEN`: __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Genereaz?? de aici [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT`: __ID-ul canalului/grupului unde botul red?? muzic??.__

6. `STARTUP_STREAM`: __Acest lucru va fi transmis ??n stream la pornirile ??i repornirile botului.
Pute??i folosi fie orice STREAM_URL, fie un link direct c??tre orice videoclip sau un link YouTube Live.
Pute??i utiliza, de asemenea, lista de redare YouTube. G??si??i un link Telegram pentru lista dvs. de redare de la [PlayList Dumb](https://telegram.dog/DumpPlaylist) sau ob??ine??i o list?? de redare de la [PlayList Extract](https://telegram.dog/GetAPlaylistbot) .
Linkul Playlist ar trebui s?? aib?? forma ???https://t.me/DumpPlaylist/xxx???.
De asemenea, pute??i utiliza fi??ierele de pe un canal ca stream de pornire. Pentru aceasta, trebuie doar s?? utiliza??i ID-ul canalului sau numele de utilizator al canalului ca valoare STARTUP_STREAM.
Pentru mai multe informa??ii despre redarea canalului, citi??i ajutorul din sec??iunea playerului.__

**Varii op??ionale recomandate**

1. `DATABASE_URI`: __MongoDB baza de date URL, ob??ine??i de la [mongodb](https://cloud.mongodb.com). Aceasta este o variant?? op??ional??, dar este recomandat s?? o utiliza??i pentru a experimenta toate func??iile.__

2. `HEROKU_API_KEY`: __Cheia dvs. API Heroku. Ob??ine??i unul de [aici](https://dashboard.heroku.com/account/applications/authorizations/new)__

3. `HEROKU_APP_NAME`: __Numele aplica??iei dvs. Heroku.__

4. `FILTRE`: __Filtre pentru c??utarea fi??ierelor de redare a canalului. Citi??i ajutor despre cplay ??n sec??iunea player.__

**Other Optional Vars**
1. `LOG_GROUP` : __Group to send Playlist, if CHAT is a Group__

2. `ADMINS` : __ID of users who can use admin commands.__

3. `REPLY_MESSAGE` : __A reply to those who message the USER account in PM. Leave it blank if you do not need this feature. (Configurable through buttons if mongodb added. Use /settings)__

4. `ADMIN_ONLY` : __Pass `True` If you want to make /play command only for admins of `CHAT`. By default /play is available for all.(Configurable through buttons if mongodb added. Use /settings)__

5. `DATABASE_NAME`: __Database name for your mongodb database.mongodb__

6. `SHUFFLE` : __Make it `False` if you dont want to shuffle playlists. (Configurable through buttons)__

7. `EDIT_TITLE` : __Make it `False` if you do not want the bot to edit video chat title according to playing song. (Configurable through buttons if mongodb added. Use /settings)__

8. `RECORDING_DUMP` : __A Channel ID with the USER account as admin, to dump video chat recordings.__

9. `RECORDING_TITLE`: __A custom title for your videochat recordings.__

10. `TIME_ZONE` : __Time Zone of your country, by default IST__

11. `IS_VIDEO_RECORD` : __Make it `False` if you do not want to record video, and only audio will be recorded.(Configurable through buttons if mongodb added. Use /record)__

12. `IS_LOOP` ; __Make it `False` if you do not want 24 / 7 Video Chat. (Configurable through buttons if mongodb added.Use /settings)__

13. `IS_VIDEO` : __Make it `False` if you want to use the player as a musicplayer without video. (Configurable through buttons if mongodb added. Use /settings)__

14. `PORTRAIT`: __Make it `True` if you want the video recording in portrait mode. (Configurable through buttons if mongodb added. Use /record)__

15. `DELAY` : __Choose the time limit for commands deletion. 10 sec by default.__

16. `QUALITY` : __Customize the quality of video chat, use one of `high`, `medium`, `low` . __

17. `BITRATE` : __Bitrate of audio (Not recommended to change).__

18. `FPS` : __Fps of video to be played (Not recommended to change.)__

"""
