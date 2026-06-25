import os
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# Webhook-ul Discord vine din "Secret" (criptat, nu e in cod)
WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "").strip()

# Ora Romaniei, cu trecere automata vara/iarna
RO = ZoneInfo("Europe/Bucharest")

# Reminderele (ora Romaniei). Botul ruleaza des si trimite cand se potriveste ora.
REMINDERS = {
    "10:00": "@everyone\n☕ **Trezirea** — cafea si pornim ziua.",
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
    print("Ora Romania acum:", now.strftime("%H:%M"))

    sent = False
    for t, msg in REMINDERS.items():
        diff = now_min - to_minutes(t)
        # trimite daca suntem la ora tinta sau pana la 4 minute dupa (toleranta pt intarziere)
        if if True:
            send(msg)
            sent = True
    if not sent:
        print("Nicio notificare la ora asta.")

if __name__ == "__main__":
    main()
