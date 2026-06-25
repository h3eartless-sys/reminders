import os
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "").strip()
RO = ZoneInfo("Europe/Bucharest")

# Mesajul de dimineata, in functie de ziua saptamanii (0=luni ... 6=duminica)
MORNING = {
    0: "@everyone\n☀️ **Buna dimineata!** 🔥 Azi e zi de **CONTENT**. Hai ca poti! Dar bea cafeaua intai. ☕",
    1: "@everyone\n☀️ **Dimineata!** 💅 Azi e zi de **LASHES**. O zi productiva te asteapta — cafea si la treaba.",
    2: "@everyone\n☀️ **Buna dimineata!** 🎬 Miercuri = **CONTENT**. Esti pe val, tine-o tot asa. ☕",
    3: "@everyone\n☀️ **Salut!** 💅 Zi de **LASHES** azi. Aproape de weekend, mai tragem putin. Cafeaua intai.",
    4: "@everyone\n☀️ **Dimineata!** 💅 Vineri = **LASHES**. Ultima zi de munca grea, apoi weekendul cu Rusty. Hai!",
    5: "@everyone\n☀️ **Buna dimineata!** 🦝 Weekend = **RUSTY**. Azi te joci cu ce-ti place. Liber la sala. ☕",
    6: "@everyone\n☀️ **Salut!** 🦝 Duminica = **RUSTY** + recuperare. Zi mai lejera, bucura-te de ea.",
}

# Reminderele fixe peste zi (la fel in fiecare zi)
REMINDERS = {
    "10:50": "@everyone\n💪 **Antrenament in 10 minute** — pregateste-te.",
    "11:00": "@everyone\n💪 **ANTRENAMENT** — e ora de forta. Hai!",
    "14:05": "@everyone\n🗑️ **STERGE MESAJUL** — au trecut 23h. Sterge-l acum!",
    "15:00": "@everyone\n📲 **REDDIT + post** — posteaza pe ambele SI trimite mesajul.",
    "18:00": "@everyone\n🏃 **BANDA** — 30 de minute, te resetezi.",
}

def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

def send(content):
    if not WEBHOOK:
        print("EROARE: lipseste secretul DISCORD_WEBHOOK")
        return
    data = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "rusty-bot"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            print("Trimis OK, status:", r.status)
    except Exception as e:
        print("Eroare la trimitere:", e)

def main():
    now = datetime.now(RO)
    now_min = now.hour * 60 + now.minute
    weekday = now.weekday()
    print("Ora Romania acum:", now.strftime("%H:%M"), "| zi:", weekday)

    sent = False

    diff_morning = now_min - to_minutes("10:00")
    if 0 <= diff_morning <= 4:
        send(MORNING[weekday])
        sent = True

    for t, msg in REMINDERS.items():
        diff = now_min - to_minutes(t)
        if 0 <= diff <= 4:
            send(msg)
            sent = True

    if not sent:
        print("Nicio notificare la ora asta.")

if __name__ == "__main__":
    main()
