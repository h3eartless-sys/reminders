import os
import json
import urllib.request

WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "").strip()

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
    send("@everyone\n🦝 TEST — daca vezi asta, botul merge!")

if __name__ == "__main__":
    main()
