# Ctrl+Curious: how each daily issue is built

The daily run fills `email/template.html` and sends it with Resend.

## Placeholders in template.html

| Placeholder | What goes in |
|---|---|
| `{{DATE_LONG}}` | e.g. `Friday, 16 October 2026` (IST date) |
| `{{ISSUE}}` | three digits, e.g. `002` (see numbering below) |
| `{{PREHEADER}}` | one plain line under 110 characters teasing today's issue |
| `{{SUMMARY_HTML}}` | 3–4 sentence paragraph; every claim is a link (format below) |
| `{{READ_ROWS}}` | 5 read rows (format below) |
| `{{WATCH_ROWS}}` | 3 watch rows (format below) |
| `{{EVENT_CARDS}}` | 1–3 event cards (format below). If there are no verified events, delete everything from `<!-- MEETUP_START -->` to `<!-- MEETUP_END -->`. |

Issue numbering: issue 001 was Thursday 15 October 2026. Count weekdays (Mon–Fri) from that date up to and including today. 16 Oct 2026 is 002, 19 Oct 2026 is 003.

## Writing rules

- Sentence case everywhere. No ALL CAPS text, no italics, no emoji.
- Never invent a story, video, event, date, venue or price. If a detail is unknown, leave it out.
- Escape `&` as `&amp;` in text, and use the real `https://` link for every item.
- Summaries are your own words. Never quote more than a few words from a source.

## Summary link format

```html
<a href="URL" style="color:#2E1F25;text-decoration:underline;text-decoration-color:#8A2E3B;">linked phrase</a>
```

## Read row (use `padding-bottom:24px` on both cells for rows 1–4, and leave it off row 5)

```html
<tr><td valign="top" width="40" style="font-size:15px;line-height:27px;color:#8A2E3B;padding-bottom:24px;">01</td><td valign="top" style="padding-bottom:24px;"><a href="URL" style="font-size:20px;line-height:27px;font-weight:600;color:#2E1F25;text-decoration:none;">Title in sentence case</a><div style="font-size:15px;line-height:23px;color:#5E4B53;padding-top:4px;">Source name · One-line summary.</div></td></tr>
```

## Watch row (rows 1–2: thumb cell `padding:0 18px 24px 0` and text cell `padding-bottom:24px`; row 3: thumb cell `padding:0 18px 0 0` and no padding on the text cell)

```html
<tr><td class="thumb" valign="top" width="168" style="padding:0 18px 24px 0;"><a href="https://www.youtube.com/watch?v=VIDEO_ID"><img src="https://img.youtube.com/vi/VIDEO_ID/mqdefault.jpg" width="168" height="95" alt="Video thumbnail" style="display:block;border:0;width:168px;height:95px;background-color:#7E4B6B;"></a></td><td valign="top" style="padding-bottom:24px;"><a href="https://www.youtube.com/watch?v=VIDEO_ID" style="font-size:19px;line-height:26px;font-weight:600;color:#2E1F25;text-decoration:none;">Video title</a><div style="font-size:15px;line-height:23px;color:#5E4B53;padding-top:4px;">Channel name · Why it is worth watching.</div></td></tr>
```

## Event card (last card: drop `margin-bottom:12px;`)

Tag for in-person: `<span style="background-color:#7E4B6B;color:#F4EEE8;padding:0 7px;">Bengaluru</span>`
Tag for online: `<span style="background-color:#C9A7B5;color:#2E1F25;padding:0 7px;">Online</span>`

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F4EEE8" background="https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/grain_paper.jpg" style="background-color:#F4EEE8;background-image:url('https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/assets/email/grain_paper.jpg');background-repeat:repeat;margin-bottom:12px;"><tr>
<td width="62" align="center" valign="middle" style="padding:14px 0 14px 12px;"><div style="font-size:30px;line-height:30px;font-weight:600;color:#8A2E3B;">DD</div><div style="font-size:14px;color:#5E4B53;">Mon</div></td>
<td width="14" style="border-right:1px solid #D9C3B7;">&nbsp;</td>
<td valign="middle" style="padding:14px 12px 14px 18px;"><div style="font-size:18px;line-height:24px;font-weight:600;">Event name</div><div style="font-size:14px;line-height:21px;color:#5E4B53;">TAG&nbsp; Known details only, e.g. Saturday · Host · Area</div></td>
<td valign="middle" align="right" style="padding-right:16px;white-space:nowrap;"><a href="URL" style="font-size:14px;color:#8A2E3B;text-decoration:none;">Details →</a></td>
</tr></table>
```
