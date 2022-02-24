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
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "VCPlayerBot")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)


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
__Puteți reda folosind oricare dintre aceste opțiuni__

1. Redați un videoclip de la un link YouTube.
Comanda: **/play**
__Puteți folosi acest lucru ca răspuns la un link YouTube sau transmiteți link-ul împreună cu o comandă. sau ca răspuns la mesaj pentru a căuta pe YouTube.__

2. Redați dintr-un fișier telegram.
Comanda: **/play**
__Răspundeți la un suport media acceptat (video și documente sau fișier audio).__
Notă: __Pentru ambele cazuri, /fplay poate fi folosit și de administratori pentru a reda melodia imediat, fără a aștepta să se termine coada.__

3. Redați dintr-o listă de redare YouTube
Comanda: **/yplay**
__Mai întâi obțineți un fișier de playlist de la @GetPlaylistBot sau @DumpPlaylist și răspundeți la fișierul de playlist.__

4. Live Stream
Comanda: **/stream**
__Trimiteți o adresă URL a streamului live sau orice adresă URL directă pentru a-l reda ca stream.__

5. Importați o listă de redare veche.
Comanda: **/import**
__Răspundeți la un fișier de listă de redare exportat anterior. __

6. Redare canal
Comanda: **/cplay**
__Utilizați `/cplay nume de utilizator al canalului sau id-ul canalului` pentru a reda toate fișierele de pe canalul dat.
În mod implicit, vor fi redate atât fișierele video, cât și documentele. Puteți adăuga sau elimina tipul de fișier folosind `FILTER` var.
De exemplu, pentru a transmite în stream audio, video și documente de pe canal, utilizați `/env FILTERS video document audio` . Dacă aveți nevoie doar de audio, puteți utiliza `/env FILTERS video audio` și așa mai departe.
Pentru a configura fișierele de pe un canal ca STARTUP_STREAM, astfel încât fișierele să fie adăugate automat la lista de redare la pornirea botului. utilizați `/env STARTUP_STREAM nume de utilizator al canalului sau id-ul canalului`

Rețineți că pentru canalele publice ar trebui să utilizați numele de utilizator al canalelor împreună cu „@”, iar pentru canalele private ar trebui să utilizați ID-ul canalului.
Pentru canalele private, asigurați-vă că atât botul, cât și contul USER sunt membri ai canalului.__
"""
    SETTINGS_HELP="""
** Vă puteți personaliza cu ușurință playerul în funcție de nevoi. Sunt disponibile următoarele configurații:**

🔹Comandă: **/settings**

🔹CONFIGURAȚII DISPONIBILE:

**Modul Player** - __Acest lucru vă permite să rulați playerul ca player muzical 24/7 sau numai atunci când există o melodie în coadă.
Dacă este dezactivat, playerul va părăsi apelul când lista de redare este goală.
În caz contrar, STARTUP_STREAM va fi transmis în stream când id-ul listei de redare este gol.__

**Video Enabled** - __Acest lucru vă permite să comutați între audio și video.
dacă este dezactivat, fișierele video vor fi redate ca audio.__

**Numai administrator** - __Activarea acestei opțiuni va restricționa utilizatorii care nu sunt administratori să folosească comanda de redare.__

**Editează titlul** - __Activând această opțiune, se va edita titlul VideoChat-ului la numele melodiilor în curs de redare.__

**Mod aleatoriu** - __Activarea acestui lucru va amesteca lista de redare ori de câte ori importați o listă de redare sau utilizați /yplay __

**Răspuns automat** - __Alegeți dacă doriți să răspundeți la mesajele PM ale contului de utilizator în redare.
Puteți configura un mesaj de răspuns personalizat folosind `REPLY_MESSAGE` confug.__

"""
    SCHEDULER_HELP="""
__VCPlayer vă permite să programați un stream.
Aceasta înseamnă că puteți programa un stream pentru o dată viitoare, iar la data programată, streamul va fi redat automat.
În prezent puteți programa un stream chiar și pentru un an!!. Asigurați-vă că ați configurat o bază de date, altfel vă veți pierde programele de fiecare dată când playerul repornește. __

Comanda: **/schedule**

__Răspundeți la un fișier sau un videoclip de pe youtube sau chiar la un mesaj text cu comanda de programare.
Media cu răspuns sau videoclipul de pe youtube va fi programat și va fi redat la data programată.
Ora de programare este implicit în IST și puteți schimba fusul orar folosind configurația `TIME_ZONE`.__

Comanda: **/slist**
__Vizualizați streamurile dvs. programate curente.__

Comanda: **/cancel**
__Anulați un program după id-ul său de program, puteți obține ID-ul programului folosind comanda /slist__

Comanda: **/cancelall**
__Anulează toate streamurile programate__
"""
    RECORDER_HELP="""
__Cu VCPlayer vă puteți înregistra cu ușurință toate conversațiile video.
În mod implicit, telegram vă permite să înregistrați pentru o durată maximă de 4 ore.
O încercare de a depăși această limită a fost făcută prin repornirea automată a înregistrării după 4 ore__

Comanda: **/record**

CONFIGURAȚII DISPONIBILE:
1. Înregistrare video: __Dacă este activat, atât videoclipul, cât și sunetul streamului vor fi înregistrate, altfel doar audio va fi înregistrat.__

2. Dimensiunea video: __Alegeți între dimensiunile portret și peisaj pentru înregistrarea dvs.__

3. Titlu de înregistrare personalizat: __Configurați un titlu de înregistrare personalizat pentru înregistrările dvs. Utilizați o comandă /rtitle pentru a configura acest lucru.
Pentru a dezactiva titlul personalizat, utilizați `/rtitle False `__

4. Înregistrare stupidă: __Puteți configura redirecționarea tuturor înregistrărilor dvs. către un canal, acest lucru va fi util deoarece, altfel, înregistrările sunt trimise către mesajele salvate din contul de streaming.
Configurați folosind configurația `RECORDING_DUMP`.__

⚠️ Dacă începeți o înregistrare cu vcplayer, asigurați-vă că opriți același lucru cu vcplayer.

"""

    CONTROL_HELP="""
__VCPlayer vă permite să vă controlați streamurile cu ușurință__
1. Sari peste o melodie.
Comanda: **/skip**
__Puteți trece un număr mai mare de 2 pentru a sări peste melodia în acea poziție.__

2. Întrerupeți playerul.
Comanda: **/pauză**

3. Reluați playerul.
Comanda: **/reluare**

4. Schimbați volumul.
Comanda: **/volum**
__Treceți volumul între 1-200.__

5. Părăsiți VC.
Comanda: **/leave**

6. Amestecați lista de redare.
Comanda: **/shuffle**

7. Ștergeți lista curentă de redare.
Comanda: **/clearplaylist**

8. Căutați videoclipul.
Comanda: **/seek**
__Puteți trece un număr de secunde pentru a fi sărit. Exemplu: /seek 10 pentru a sări peste 10 sec. /seek -10 pentru a derula înapoi 10 sec.__

9. Dezactivați sunetul playerului.
Comanda: **/vcmute**

10. Activați sunetul playerului.
Comanda: **/vcunmute**

11. Afișează lista de redare.
Comanda: **/playlist**
__Folosiți /player pentru a afișa cu butoanele de control__
"""

    ADMIN_HELP="""
__VCPlayer vă permite să controlați administratorii, adică puteți adăuga administratori și îi puteți elimina cu ușurință.
Este recomandat să utilizați o bază de date MongoDb pentru o experiență mai bună, altfel toți administratorii dvs. vor fi resetati după repornire.__

Comanda: **/vcpromote**
__Puteți promova un administrator cu numele de utilizator sau id-ul de utilizator sau răspunzând la mesajul respectiv.__

Comanda: **/vcdemote**
__Eliminați un administrator din lista de administratori__

Comanda: **/refresh**
__Actualizați lista de administratori a chat__
"""

    MISC_HELP="""
Comanda: **/export**
__VCPlayer vă permite să exportați lista de redare curentă pentru o utilizare viitoare.__
__Vă fi trimis un fișier json și același lucru poate fi folosit împreună cu comanda /import.__

Comanda: **/logs**
__Dacă playerul dvs. a mers prost, puteți verifica cu ușurință jurnalele folosind /logs__
 
Comanda: **/env**
__Configurați config vars cu comanda /env.__
__Exemplu: pentru a configura un__ `REPLY_MESSAGE` __use__ `/env REPLY_MESSAGE=Hei, verificați @subin_works în loc să trimiteți spam în PM`__
__Puteți șterge o config var omitând o valoare pentru aceasta, Exemplu:__ `/env LOG_GROUP=` __acest lucru va șterge configurația existentă LOG_GROUP.

Comanda: **/config**
__La fel cu utilizarea /env**

Comanda: **/update**
__Actualizează dvs. bot cu cele mai recente modificări__

Sfat: __Puteți schimba cu ușurință configurația CHAT adăugând contul de utilizator și contul bot la orice alt grup și orice comandă din grupul nou__

"""
    ENV_HELP="""
**Acestea sunt variantele configurabile disponibile și le puteți seta pe fiecare folosind comanda /env**


**Vars obligatorii**

1. `API_ID`: __Get From [my.telegram.org](https://my.telegram.org/)__

2. `API_HASH` : __Obțineți de la [my.telegram.org](https://my.telegram.org)__

3. `BOT_TOKEN`: __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Generează de aici [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT`: __ID-ul canalului/grupului unde botul redă muzică.__

6. `STARTUP_STREAM`: __Acest lucru va fi transmis în stream la pornirile și repornirile botului.
Puteți folosi fie orice STREAM_URL, fie un link direct către orice videoclip sau un link YouTube Live.
Puteți utiliza, de asemenea, lista de redare YouTube. Găsiți un link Telegram pentru lista dvs. de redare de la [PlayList Dumb](https://telegram.dog/DumpPlaylist) sau obțineți o listă de redare de la [PlayList Extract](https://telegram.dog/GetAPlaylistbot) .
Linkul Playlist ar trebui să aibă forma „https://t.me/DumpPlaylist/xxx”.
De asemenea, puteți utiliza fișierele de pe un canal ca stream de pornire. Pentru aceasta, trebuie doar să utilizați ID-ul canalului sau numele de utilizator al canalului ca valoare STARTUP_STREAM.
Pentru mai multe informații despre redarea canalului, citiți ajutorul din secțiunea playerului.__

**Varii opționale recomandate**

1. `DATABASE_URI`: __MongoDB baza de date URL, obțineți de la [mongodb](https://cloud.mongodb.com). Aceasta este o variantă opțională, dar este recomandat să o utilizați pentru a experimenta toate funcțiile.__

2. `HEROKU_API_KEY`: __Cheia dvs. API Heroku. Obțineți unul de [aici](https://dashboard.heroku.com/account/applications/authorizations/new)__

3. `HEROKU_APP_NAME`: __Numele aplicației dvs. Heroku.__

4. `FILTRE`: __Filtre pentru căutarea fișierelor de redare a canalului. Citiți ajutor despre cplay în secțiunea player.__

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
