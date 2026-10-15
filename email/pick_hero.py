"""Pick today's hero image for Ctrl+Curious.

Each weekday has its own pool of images in assets/email/days/<day>/.
The pool is shuffled once (fixed seed) and walked week by week, so every
image is used before any repeats, and a month never shows the same image twice.

Usage: python3 email/pick_hero.py [YYYY-MM-DD]   (defaults to today in IST)
Prints the public image URL, or nothing if that weekday has no pool yet.
"""
import datetime, random, sys, os

BASE = 'https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/days/'
POOLS = {0: ('mon', 8), 1: ('tue', 8), 2: ('wed', 8), 3: ('thu', 8)}        # weekday -> (folder, number of images); add tue..fri as they are made
START = datetime.date(2026, 10, 19)  # first Monday of the rotation

def pick(day):
    if day.weekday() not in POOLS:
        return None
    folder, n = POOLS[day.weekday()]
    order = list(range(1, n + 1))
    random.Random(f'ctrl-curious-{folder}').shuffle(order)
    week = (day - START).days // 7
    return f'{BASE}{folder}/{folder}_{order[week % n]:02d}.jpg'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        day = datetime.date.fromisoformat(sys.argv[1])
    else:
        day = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    url = pick(day)
    if url:
        print(url)
