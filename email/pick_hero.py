"""Pick today's hero image for Ctrl+Curious.

Each weekday has its own pool of 10 images in assets/email/days2/<day>/
(the "Use for - <day>" sets on the design canvas). The pool is shuffled once
(fixed seed) and walked week by week, so every image is used before any repeats.

Usage: python3 email/pick_hero.py [YYYY-MM-DD]          prints the image URL
       python3 email/pick_hero.py [YYYY-MM-DD] --alt    prints the URL, then its alt text on a second line
Defaults to today in IST. Prints nothing on weekends.
"""
import datetime, random, sys

BASE = 'https://ctrl-curious.vercel.app/assets/email/days2/'
POOLS = {0: ('mon', 10), 1: ('tue', 10), 2: ('wed', 10), 3: ('thu', 10), 4: ('fri', 10)}   # weekday -> (folder, number of images)
START = datetime.date(2026, 10, 19)  # first Monday of the rotation
ALTS = {
 "mon/mon_01.jpg": "A giant toggle on the horizon, the sun as its knob and the sea as its track",
 "mon/mon_02.jpg": "A tree whose branches split like a node diagram, leaves clustered at the tips",
 "mon/mon_03.jpg": "A cloud-shaped chat bubble raining onto green hills",
 "mon/mon_04.jpg": "Mountains drawn as a line chart, with a sun and a height label at the peak",
 "mon/mon_05.jpg": "A meadow of flowers whose heads are checkboxes, most of them ticked",
 "mon/mon_06.jpg": "The phases of the moon as page dots over a night sea",
 "mon/mon_07.jpg": "A big leaf whose veins are a layout grid, measured with guides",
 "mon/mon_08.jpg": "A landscape pulled apart into stacked layers, each with a wireframe label",
 "mon/mon_09.jpg": "The sun as a slider handle travelling a dotted arc over pine hills",
 "mon/mon_10.jpg": "Snow-capped mountains drawn as a bar chart under a radio-button moon",
 "tue/tue_01.jpg": "A phone on a desk, its notifications rising like bubbles toward the sun",
 "tue/tue_02.jpg": "Rows of keycaps rolling like swell, one wine key pressed",
 "tue/tue_03.jpg": "Headphones over sound bars rising out of the sea",
 "tue/tue_04.jpg": "A code editor at night, code as coloured bars and a blinking cursor",
 "tue/tue_05.jpg": "A progress ring around the sun at 72%, a progress bar on the horizon of a teal sea",
 "tue/tue_06.jpg": "Wifi arcs rising from a small router like a sunrise over the sea",
 "tue/tue_07.jpg": "A microchip with circuit lines flowing out like rivers",
 "tue/tue_08.jpg": "Server towers under the moon, their status lights like a city at night",
 "tue/tue_09.jpg": "An open laptop whose screen holds the sun over swell lines",
 "tue/tue_10.jpg": "A cursor mid-click, the click spreading out in rings",
 "wed/wed_01.jpg": "Aa set in Fraunces on plum with specimen guide lines",
 "wed/wed_02.jpg": "Ww in DM Serif Display filled with wave stripes, a wine sun behind",
 "wed/wed_03.jpg": "A teal ampersand beside a breaking wave",
 "wed/wed_04.jpg": "A specimen grid of coloured tiles, one Young Serif letter each",
 "wed/wed_05.jpg": "An outline g in Playfair Display with baseline, x-height and descender guides",
 "wed/wed_06.jpg": "Rr, Gg and Qq in three typefaces with wave rules between",
 "wed/wed_07.jpg": "The letter o as a moon rising over a woodblock sea",
 "wed/wed_08.jpg": "Hamburgefonstiv in Bricolage Grotesque across three weights",
 "wed/wed_09.jpg": "The pair AV in Syne tucked together, with a kerning bracket marking -70",
 "wed/wed_10.jpg": "Aa in DM Serif Display at six sizes, growing like a building swell",
 "thu/thu_01.jpg": "Three clusters of sticky notes on a dotted board, each under a circle label",
 "thu/thu_02.jpg": "Idea, test and ship as basic shapes joined by wavy connectors ending at the sun",
 "thu/thu_03.jpg": "A sticky note collecting reaction stamps, a big +1 landing like a sun",
 "thu/thu_04.jpg": "A labelled section of basic shapes, a teammate dragging a star out",
 "thu/thu_05.jpg": "A marker drawing a swell across a dotted board between two stickies",
 "thu/thu_06.jpg": "Four teammates’ cursors with name tags heading for one ochre circle",
 "thu/thu_07.jpg": "A row of sticky notes with vote dots, one clearly winning",
 "thu/thu_08.jpg": "Basic shapes stacked into a balancing tower under a circle sun",
 "thu/thu_09.jpg": "Sticky notes on a dotted teal board joined by an ochre connector",
 "thu/thu_10.jpg": "Triangle mountains, a circle sun and pill-shaped swell, a teammate’s cursor selecting them",
 "fri/fri_01.jpg": "A pixel laptop closing for the weekend, a mug and a plant beside it",
 "fri/fri_02.jpg": "A cascade of too many pixel browser windows",
 "fri/fri_03.jpg": "A pixel beach with an umbrella, a towel, blocky waves and a big sun",
 "fri/fri_04.jpg": "A pixel tent and campfire under a moon between pine trees",
 "fri/fri_05.jpg": "A beige pixel computer showing a wave, with keyboard and mouse",
 "fri/fri_06.jpg": "A pixel calendar page with the weekend lit up",
 "fri/fri_07.jpg": "A pixel bicycle on a seaside path at sunset",
 "fri/fri_08.jpg": "A pixel book and steaming mug by a rainy window",
 "fri/fri_09.jpg": "A pixel cinema screen showing the sea, a row of heads watching",
 "fri/fri_10.jpg": "A pixel bed with a wave blanket, morning sun and a clock at 10:30"
}

def pick(day):
    """Return (url, alt) for that day, or None on weekends."""
    if day.weekday() not in POOLS:
        return None
    folder, n = POOLS[day.weekday()]
    order = list(range(1, n + 1))
    random.Random(f'ctrl-curious-{folder}').shuffle(order)
    week = (day - START).days // 7
    name = f'{folder}/{folder}_{order[week % n]:02d}.jpg'
    return BASE + name, ALTS.get(name, '')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--alt']
    if args:
        day = datetime.date.fromisoformat(args[0])
    else:
        day = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()
    got = pick(day)
    if got:
        print(got[0])
        if '--alt' in sys.argv:
            print(got[1])
