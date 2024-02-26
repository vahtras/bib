import datetime
import json

def check():
    with open("token.json") as tf:
        expiry = json.load(tf)['expiry']
    expires = datetime.datetime.fromisoformat(expiry)

    now = datetime.datetime.now(tz=expires.tzinfo)
    return  expires < now

if __name__ == "__main__":
    print("Valid" if check() else "Expired")
