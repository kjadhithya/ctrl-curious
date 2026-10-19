# Ctrl+Curious: how each daily issue is built

The daily run fills `email/template.html` and sends it with Resend.

## Placeholders in template.html

| Placeholder | What goes in |
|---|---|
| `{{DATE_LONG}}` | e.g. `Friday, 16 October 2026` (IST date) |
| `{{ISSUE}}` | three digits, e.g. `002` (see numbering below) |
| `{{PREHEADER}}` | one plain line under 110 characters teasing today's issue |
| `{{HERO_URL}}` | today's hero image URL (see Hero image below) |
| `{{SUMMARY_HTML}}` | 3–4 sentence paragraph; every claim is a link (format below) |
| `{{READ_ROWS}}` | 5 read rows (format below) |
| `{{WATCH_ROWS}}` | 3 watch rows (format below) |
| `{{UNSUB_URL}}` | `https://ctrl-curious.vercel.app/unsubscribe` in the copy sent to the editor; `https://ctrl-curious.vercel.app/unsubscribe?e=` plus the subscriber's percent-encoded email in each subscriber's copy |
| `{{EVENT_CARDS}}` | 1–3 event cards (format below). If there are no verified events, delete everything from `<!-- MEETUP_START -->` to `<!-- MEETUP_END -->`. |

Issue numbering: issue 001 was Thursday 15 October 2026. Count weekdays (Mon–Fri) from that date up to and including today. 16 Oct 2026 is 002, 19 Oct 2026 is 003.

## Hero image

Each weekday has its own rotating set of hero images. Get today's URL with:

```
curl -sSL https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/email/pick_hero.py -o pick_hero.py
python3 pick_hero.py
```

Use the URL it prints for `{{HERO_URL}}`. If it prints nothing (that weekday has no set yet), use
`https://ctrl-curious.vercel.app/assets/email/wave_hero.jpg`.

## Sending

There are two sends, and each happens exactly once per run.

1. **The editor's copy, through Resend.** Send one email to kjadhithya05@gmail.com with the Resend send-email tool (details in the task prompt). Once it returns an email ID, it is sent: never send it again, even to retry or test. Retry only if the call returned an error and no ID.

2. **Subscribers: do not email them from this run.** The Gmail tool strips every image, so subscriber copies and welcome emails are sent by the editor's Google Apps Script instead. It checks the website every five minutes, and as soon as today's email file is published (see "Publishing to the website") it sends each subscriber their own copy with images and a personal unsubscribe link, and welcomes anyone new. Your job is only to publish the files below promptly, right after the editor's copy is sent. Never call the Gmail send tool for subscribers or welcomes.

## Edition sections (one extra section per weekday)

Each weekday has its own edition, and each edition adds one section to the usual summary, Read, Watch and Meet up. Research it with the same care as the reads: real, recent, verified, with a working link, and useful to designers who already know the basics. If you cannot verify a good one, leave that section out (omit its key); never invent one. Put it in the issue JSON under `"edition"`.

**How to research the edition section (do this properly, it is the most distinctive part of each issue):**
- Spend real effort here: run at least five or six different searches and look at several sources before choosing. Never take the first result.
- Fresh means new or newly updated in the last two weeks (the last month at most for typefaces and case studies), with the date confirmed on the maker's own page.
- Trending means people in the design community are actually talking about it: covered by more than one credible source, featured by the maker's community or a respected newsletter, climbing on Product Hunt or Figma Community, or shared by well-known designers. Prefer something with that signal over something merely new.
- Build a shortlist of three to five candidates, compare them on freshness, how much buzz they have, and how useful they are to working designers, then pick the strongest. Mention in your final message which candidates you considered and why you chose the winner.
- Where to look: for tools, Product Hunt (design and AI), Figma Community and release notes, Framer, Adobe, Webflow and AI design tool blogs, and design newsletters. For typefaces, foundry news pages, Google Fonts' new additions, Creative Boom's type drop, I Love Typography, Typewolf and It's Nice That. For case studies, company design blogs (Airbnb, Spotify, Duolingo, Shopify, Linear, Atlassian, Uber and others), studio project pages and Case Study Club. For the week ahead, conference and event calendars, launch schedules and awards sites.
- Never repeat a pick from a previous issue (check the last month of files in issues/).

- **Monday · Week ahead: "This week in design".** Exactly three things happening this week (Monday to Sunday), in date order: ideally one launch, release or deadline, one talk or livestream to catch, and one contest or call for entries. Each needs a confirmed date and a link.
  `"edition": {"week": [{"when": "Wednesday · Launch", "title": "What is happening, in sentence case", "url": "https://..."}, ...3 items]}`
- **Tuesday · Tools: "Tool of the day".** One tool, plugin or AI feature that is new or meaningfully updated in the last two weeks, from its maker's own page. Two sentences: what it does and the one job it is best at. `meta` is the price and platform, if known.
  `"edition": {"tool": {"name": "", "url": "https://maker.page", "what": "Two sentences.", "meta": "Free · Figma plugin"}}`
- **Wednesday · Type: "Typeface spotlight".** One typeface released or notably updated recently (foundry release, Google Fonts addition, a type-news piece). It always gets a real specimen picture, never an unrelated image:
  - If the family is on Google Fonts (free), render the specimen from its real font files: `git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts gfonts && git -C gfonts sparse-checkout set ofl/<familyname>` (lowercase, no spaces), then `python3 art/specimen/make_specimen.py --name "<Family>" --regular gfonts/ofl/<dir>/<Family>-Regular.ttf [--italic …] [--bold …] --line "One short line about it" --out assets/email/specimens/<familyname>.jpg`, look at the picture, and set `"image": "https://ctrl-curious.vercel.app/assets/email/specimens/<familyname>.jpg"`. Commit the jpg with the issue.
  - If it is paid, link the foundry or specimen page; leave out `image` and the foundry page's own share image is shown. Only pick a paid family whose page has a proper specimen image.
  `"edition": {"typeface": {"name": "", "url": "https://foundry/specimen", "by": "Designer, foundry", "get": "Google Fonts (free)" or "Foundry site (paid)", "pair": "One pairing idea", "good_for": "Headlines, editorial, UI", "note": "One or two sentences on what makes it notable.", "image": "optional specimen URL"}}`
- **Thursday · Case study: "Case study".** One real case study published recently by the team or studio that did the work (a company design blog, a studio's project page, a detailed write-up). Not a concept by someone unconnected to the product.
  `"edition": {"case": {"title": "", "url": "https://...", "studio": "Studio or team", "client": "Client, if any", "note": "The problem in one line, what they made, and the one decision that made it work."}}`
- **Friday · Weekend: "Weekend watchlist" and "Inspiration shelf".** Five videos instead of three (same rules as Watch; five different channels); put the best long one first, since it is shown big, and ideally include a talk or studio visit and something lighter. They go in `watch`, and the section is titled and laid out automatically. Then the Inspiration shelf: three pieces of recent, real work worth looking at over the weekend, ideally a poster or piece of graphic design, an interface, and a small product detail, each linked to the maker's own page (studio site, Behance, the product's own post), since that page's share image is shown. Credit the designer, studio or product.
  `"edition": {"shelf": [{"title": "What it is", "credit": "Designer, studio or product", "url": "https://..."}, ...3 items]}`

## Practical sections (go in `"edition": {"learn": [...]}`, next to the day's other edition key)

These sections are for designers who want to work better this week and keep learning. Each must be something a reader can use straight away and must teach them something they probably don't already know, grounded in a real source you have actually read (an article, docs page, talk or post, from the last two weeks where possible). Write the steps yourself from what the source says; if a step is your own advice rather than the source's, say so in `take`. Research these as carefully as the edition section: shortlist a few candidates, pick the most useful and timely, and never repeat a topic from the last month. Avoid topics every designer already knows; if the idea is familiar, the section must add something new, like concrete design tips.

Which ones go on which day (the headings are set by the builder):
- **Monday:** `skill` (Skill of the week) and `prompt` (Prompt of the week)
- **Tuesday:** `tool` (Tool to master)
- **Wednesday:** `steal` (Steal this) and `brief` (10-minute brief)
- **Thursday:** `people` (How they work) and `decision` (Decision toolkit)
- **Friday:** `install` (Power-up)

What each one is, and the fields it uses (every item needs `kind`, `title`, `url`, `intro` and at least one `links` entry `{"title", "url", "source", "anchor"}`; `take` is optional and shows as "Our take"). There is no separate "More" line: each link is placed on its `anchor`, a short phrase copied exactly from the section's own text (intro, steps, tips, changes, define, why, take, code_note, try or an example). Pick a phrase that reads naturally as the link, and give each link a different phrase. The builder prints a warning if a link can't be placed; fix the anchor before sending:
- `skill` (Skill of the week): one practical method a designer can apply this week (research, AI workflows, systems, accessibility, writing, working with engineers). `steps`: 3 to 5 short steps.
- `prompt`: one tested AI prompt for a real design job (critique, synthesis, UX copy, edge cases). `tool`: which assistant it is for ("Any AI assistant" is fine); `code`: the prompt, ready to copy, with [brackets] for what the reader fills in; `code_note`: how to use it; `columns`: two lists, `{"label": "Use it for", "items": [2 items]}` and `{"label": "Not for", "items": [2 items]}`.
- `tool` (Tool to master): a deeper workflow in a tool designers already use, beyond "what's new": `steps`: 3 to 5 moves that save real time, from the tool's own docs; `take` for plan or seat limits.
- `steal`: one free, ready-to-use asset (template, checklist, agenda, file format, starter file). `file`: a file name for the tab (like "review-agenda.md"); `code`: the usable excerpt; `code_note`: how to use it; `meta`: "Free · from …"; the url is the original.
- `brief` (10-minute brief): one idea explained plainly that most designers don't fully know yet, and how to design for it. `define`: a one-sentence definition; `examples`: 3 `{"name", "text", "url"}` (where it showed up this week, or who it affects; set `examples_label` if not "Where it showed up this week"); `tips`: 3 to 5 concrete design tips (set `tips_label` if not "How to design for it"); `why`: why it matters to the reader's work.
- `people` (How they work): a respected designer or design team and how they work, from their own interview, talk or post. `person`: `{"name", "role", "initials"}`; `steps`: 3 habits worth copying; `source_line`: e.g. "From Dive Club · our takeaways from the episode".
- `decision` (Decision toolkit): a framework for a recurring call (where AI help lives, which navigation pattern, when to push back). `columns`: two `{"label": "X when", "items": [3 items]}` lists; `examples`: one real product `{"name", "text", "url"}`; `rule`: a one-line rule of thumb.
- `install` (Power-up): one ready-made skill, plugin or agent instruction set that makes an AI tool better at design work, checked on its maker's own page (for example Anthropic's public skills at github.com/anthropics/skills, Figma agent skills, Framer skills). `skill`: `{"name", "by", "cost"}`; `changes`: 3 or 4 things it changes about how the tool works; `install`: 1 or 2 ways to get it, `{"where", "how", "code"}` (`code` only for commands), taken from the maker's instructions; `try`: one request to try first. Never repeat one from the last two months.

## Writing rules

- Sentence case everywhere. No ALL CAPS text, no italics, no emoji.
- Never invent a story, video, event, date, venue or price. If a detail is unknown, leave it out.
- Escape `&` as `&amp;` in text, and use the real `https://` link for every item.
- Summaries are your own words. Never quote more than a few words from a source.

## Who it's for and what every item must do

The readers are senior product designers, UX/UI designers, design leads and experts. They already know the fundamentals, so skip anything introductory: no 101 guides, glossaries, basic how-tos, "tips for beginners" or listicles. Every read, video and meetup must do at least one of two jobs at a senior level:

1. **Help them upskill**: advanced practice, new methods, original research or hard-won lessons from experienced teams that a senior designer can apply at work (research methods, interaction and UI patterns, design systems, accessibility, prototyping, AI in the design workflow, writing for interfaces, working with engineers and PMs, presenting and influencing).
2. **Keep them current**: what is changing in product and UX/UI design right now (tool launches and major updates in Figma, Framer, Adobe and AI design tools; shifts in how teams work; notable app and product redesigns; industry moves; design news from India).

Before including anything, ask: would a product designer be better at their job, or better informed about their field, after this? If not, drop it.

## Choosing the Read stories

- Aim for a balance across the five: roughly two to upskill (original research, deep analysis, case studies from real teams) and three to stay current (news, launches, breakdowns of real shipped redesigns, trend analysis). Never five pieces of news with nothing to learn from.
- Credibility matters: prefer recognised publications, established researchers, design leaders and the teams that actually built the product. Skip personal concept redesigns of other companies' products by people with no connection to them, however polished.
- Best sources: UX Collective (uxdesign.cc), Smashing Magazine, Nielsen Norman Group, Figma blog and Config talks, Bootcamp, UX Planet, Built for Mars, Lenny's Newsletter design posts, Intercom and Linear and Stripe design blogs, Sidebar.io picks, company design blogs (Airbnb, Uber, Spotify, Atlassian, Shopify Polaris, Google Material), and Indian design teams (Swiggy, Zomato, Razorpay, CRED, Flipkart).
- Gallery sites (It's Nice That, Dezeen, Creative Bloq) only when the piece is about digital product or interface design. No festival identities, posters, packaging or rebrands of companies the reader has no connection to.
- Each note says what the reader gets: the technique to try, or what changed and why it matters for their work.

## Choosing the Watch videos (be picky)

The three videos follow the same rule: each must help product and UX/UI designers upskill or stay current. Aim for at least one practical video (a technique or tool walkthrough) and at least one tied to what is happening this week.

- Three different channels. Never two videos from the same channel in one issue, and avoid a channel used in the previous issue (check the last file in `issues/` on GitHub).
- Fresh: published in the last 7 days. Go up to 14 days only if nothing good is newer. Confirm the upload date on the video page itself, not from a search snippet.
- At least one video must connect to a story in today's Read list or summary, such as a launch walkthrough, a conference talk that just went up, or a first look at a new tool.
- Good sources to check first: official channels (Figma, Adobe, Framer, Webflow, Google Design, Apple Developer, Y Combinator), fresh conference talks (Config, Adobe MAX, Awwwards, Clarity, Into Design Systems), interviews with design leaders (Dive Club, Lenny's Podcast, Design Better) and research groups (NN/g). A strong video from somewhere else is welcome if the speaker has real standing.
- Not for this audience: beginner tutorials, "I redesigned X" concept videos by people unconnected to the product, and creator content aimed at people starting out.
- Skip vague motivational or career-chat videos, and anything older than a few weeks. A practical walkthrough is welcome when it teaches a real skill or shows a new tool or feature.
- Each note should say why it matters now (what is new or timely), not just what the video covers.

## Summary link format

```html
<a href="URL" target="_blank" style="color:#2E1F25;text-decoration:underline;text-decoration-color:#8A2E3B;">linked phrase</a>
```

## Read row (rows 1–4 as shown; on row 5 drop the 24px bottom padding from all three cells, so the image cell becomes `padding:4px 16px 0 0`)

The middle cell, between the number and the text, shows the article's own share image, served by the website at `https://ctrl-curious.vercel.app/api/og?url=URL_ENCODED`, where URL_ENCODED is the article URL percent-encoded (in Python: `urllib.parse.quote(url, safe='')`). Nothing needs fetching beforehand; if an article has no image, the site returns a Ctrl+Curious artwork instead.

```html
<tr><td valign="top" width="40" style="font-size:15px;line-height:27px;color:#8A2E3B;padding-bottom:24px;">01</td><td class="rthumb" valign="top" width="120" style="padding:4px 16px 24px 0;"><a href="URL" target="_blank"><img src="https://ctrl-curious.vercel.app/api/og?url=URL_ENCODED" width="120" height="63" alt="" style="display:block;border:0;width:120px;height:63px;background-color:#D9C3B7;"></a></td><td valign="top" style="padding-bottom:24px;"><a href="URL" target="_blank" style="font-size:20px;line-height:27px;font-weight:600;color:#2E1F25;text-decoration:none;">Title in sentence case</a><div style="font-size:15px;line-height:23px;color:#5E4B53;padding-top:4px;">Source name · One-line summary.</div></td></tr>
```

## Watch row (rows 1–2: thumb cell `padding:0 18px 24px 0` and text cell `padding-bottom:24px`; row 3: thumb cell `padding:0 18px 0 0` and no padding on the text cell)

```html
<tr><td class="thumb" valign="top" width="168" style="padding:0 18px 24px 0;"><a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank"><img src="https://img.youtube.com/vi/VIDEO_ID/mqdefault.jpg" width="168" height="95" alt="Video thumbnail" style="display:block;border:0;width:168px;height:95px;background-color:#7E4B6B;"></a></td><td valign="top" style="padding-bottom:24px;"><a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" style="font-size:19px;line-height:26px;font-weight:600;color:#2E1F25;text-decoration:none;">Video title</a><div style="font-size:15px;line-height:23px;color:#5E4B53;padding-top:4px;">Channel name · Why it is worth watching.</div></td></tr>
```

## Event card (last card: drop `margin-bottom:12px;`). The event name is the link; there is no separate Details button.

Tag for in-person: `<span style="background-color:#7E4B6B;color:#F4EEE8;padding:0 7px;">Bengaluru</span>`
Tag for online: `<span style="background-color:#C9A7B5;color:#2E1F25;padding:0 7px;">Online</span>`

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F4EEE8" background="https://ctrl-curious.vercel.app/assets/email/grain_paper.jpg" style="background-color:#F4EEE8;background-image:url('https://ctrl-curious.vercel.app/assets/email/grain_paper.jpg');background-repeat:repeat;margin-bottom:12px;"><tr>
<td width="62" align="center" valign="middle" style="padding:14px 0 14px 12px;"><div style="font-size:30px;line-height:30px;font-weight:600;color:#8A2E3B;">DD</div><div style="font-size:14px;color:#5E4B53;">Mon</div></td>
<td width="14" style="border-right:1px solid #D9C3B7;">&nbsp;</td>
<td valign="middle" style="padding:14px 16px 14px 18px;"><a href="URL" target="_blank" style="font-size:18px;line-height:24px;font-weight:600;color:#2E1F25;text-decoration:none;">Event name</a><div style="font-size:14px;line-height:21px;color:#5E4B53;">TAG&nbsp; Known details only, e.g. Saturday · Host · Area</div></td>
</tr></table>
```

## Building and publishing (steps 1–3 before sending the editor's copy, steps 4–5 right after; publishing is what emails subscribers)

The website is built from one JSON file per issue in `issues/` of the GitHub repo `kjadhithya/ctrl-curious`. Pushing a new file to `main` makes Vercel rebuild the site within a minute or two. Do this only after the email has been sent and returned an email ID; a failure here must never cause a resend.

1. Attach the repo with push access: call the `add_repo` tool with owner `kjadhithya`, repo `ctrl-curious`, access `push`, then run the clone command it gives you.
2. Write `issues/NNN.json` (NNN = the three-digit issue number). If the file already exists, stop: today's issue is already published. Use exactly this shape, with the same content as the email:

```json
{
  "issue": 2,
  "date": "2026-10-16",
  "title": "A headline for the day in sentence case, under about 90 characters. Say literally what happened (who did what); no metaphors or clever phrasing that needs the summary to decode it.",
  "dek": "One plain sentence listing what's inside, no links.",
  "hero": "the {{HERO_URL}} used in the email",
  "hero_alt": "Short description of the artwork",
  "summary": "The 'Today, in brief' text, with each link written as [linked phrase](https://source.url)",
  "reads": [{ "title": "", "source": "", "url": "https://...", "note": "the one-line summary" }],
  "watch": [{ "title": "", "channel": "", "id": "YouTube video ID", "note": "" }],
  "meetups": [{ "name": "", "date": "YYYY-MM-DD", "place": "Bengaluru or Online", "details": "known details only", "url": "https://..." }],
  "edition": {}
}
```

   Fill `"edition"` with today's key from 'Edition sections' (`{}` if none could be verified). Use `"meetups": []` when the Meet up section was removed. Sentence case, no ALL CAPS, no emoji.
3. The email files: `python3 email/build_issue.py issues/NNN.json email/issues/NNN.html` builds the finished email (every row, card and edition section, from the JSON) and writes `email/issues/NNN.txt`, the plain-text version, next to it. This HTML is also exactly what you send to the editor, so build it before sending.
4. Check it builds: `node site/build.mjs` must print `Built N issue(s)`. If it fails, fix the JSON (usually a quote or comma) and rerun.
5. Commit and push to `main` (all three files in one commit):
   `git add issues/NNN.json email/issues/NNN.html email/issues/NNN.txt && git -c user.name="kjadhithya" -c user.email="kjadhithya05@gmail.com" commit -m "Issue NNN: <title>" && git push origin HEAD:main`
   If the push is rejected because main moved, run `git pull --rebase origin main` and push again.
6. If the repo can't be attached or pushed, don't retry endlessly: say so in the final message and include the JSON so it can be added by hand.
