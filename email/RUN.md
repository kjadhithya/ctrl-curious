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
| `{{EVENT_CARDS}}` | 1–3 event cards (format below). If there are no verified events, delete everything from `<!-- MEETUP_START -->` to `<!-- MEETUP_END -->`. |

Issue numbering: issue 001 was Thursday 15 October 2026. Count weekdays (Mon–Fri) from that date up to and including today. 16 Oct 2026 is 002, 19 Oct 2026 is 003.

## Hero image

Each weekday has its own rotating set of hero images. Get today's URL with:

```
curl -sSL https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/email/pick_hero.py -o pick_hero.py
python3 pick_hero.py
```

Use the URL it prints for `{{HERO_URL}}`. If it prints nothing (that weekday has no set yet), use
`https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/wave_hero.jpg`.

## Sending

Send exactly one email per run. Once send-email returns an email ID, the issue is sent: do not send it again, even to retry or test. Retry only if the first call returned an error and no ID.

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
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F4EEE8" background="https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/grain_paper.jpg" style="background-color:#F4EEE8;background-image:url('https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/grain_paper.jpg');background-repeat:repeat;margin-bottom:12px;"><tr>
<td width="62" align="center" valign="middle" style="padding:14px 0 14px 12px;"><div style="font-size:30px;line-height:30px;font-weight:600;color:#8A2E3B;">DD</div><div style="font-size:14px;color:#5E4B53;">Mon</div></td>
<td width="14" style="border-right:1px solid #D9C3B7;">&nbsp;</td>
<td valign="middle" style="padding:14px 16px 14px 18px;"><a href="URL" target="_blank" style="font-size:18px;line-height:24px;font-weight:600;color:#2E1F25;text-decoration:none;">Event name</a><div style="font-size:14px;line-height:21px;color:#5E4B53;">TAG&nbsp; Known details only, e.g. Saturday · Host · Area</div></td>
</tr></table>
```

## Publishing to the website (after the email is sent)

The website is built from one JSON file per issue in `issues/` of the GitHub repo `kjadhithya/ctrl-curious`. Pushing a new file to `main` makes Vercel rebuild the site within a minute or two. Do this only after the email has been sent and returned an email ID; a failure here must never cause a resend.

1. Attach the repo with push access: call the `add_repo` tool with owner `kjadhithya`, repo `ctrl-curious`, access `push`, then run the clone command it gives you.
2. Write `issues/NNN.json` (NNN = the three-digit issue number). If the file already exists, stop: today's issue is already published. Use exactly this shape, with the same content as the email:

```json
{
  "issue": 2,
  "date": "2026-10-16",
  "title": "A headline for the day in sentence case, under about 90 characters",
  "dek": "One plain sentence listing what's inside, no links.",
  "hero": "the {{HERO_URL}} used in the email",
  "hero_alt": "Short description of the artwork",
  "summary": "The 'Today, in brief' text, with each link written as [linked phrase](https://source.url)",
  "reads": [{ "title": "", "source": "", "url": "https://...", "note": "the one-line summary" }],
  "watch": [{ "title": "", "channel": "", "id": "YouTube video ID", "note": "" }],
  "meetups": [{ "name": "", "date": "YYYY-MM-DD", "place": "Bengaluru or Online", "details": "known details only", "url": "https://..." }]
}
```

   Use `"meetups": []` when the Meet up section was removed. Sentence case, no ALL CAPS, no emoji.
3. Check it builds: `node site/build.mjs` must print `Built N issue(s)`. If it fails, fix the JSON (usually a quote or comma) and rerun.
4. Commit and push to `main`:
   `git add issues/NNN.json && git -c user.name="kjadhithya" -c user.email="kjadhithya05@gmail.com" commit -m "Issue NNN: <title>" && git push origin HEAD:main`
   If the push is rejected because main moved, run `git pull --rebase origin main` and push again.
5. If the repo can't be attached or pushed, don't retry endlessly: say so in the final message and include the JSON so it can be added by hand.
