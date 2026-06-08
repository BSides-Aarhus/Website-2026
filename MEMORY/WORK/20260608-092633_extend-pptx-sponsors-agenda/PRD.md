---
task: Extend pptx script to render sponsors, then run
slug: 20260608-092633_extend-pptx-sponsors-agenda
effort: standard
phase: complete
progress: 22/22
mode: interactive
started: 2026-06-08T09:26:33Z
updated: 2026-06-08T09:26:33Z
---

## Context

The user asked to "extend and run the script" — `scripts/build_pptx_template.py`, which
generates the BSides Aarhus 2026 deck. Goal (from the prior turn): agenda, speakers, and
sponsors should all be CURRENT in the regenerated presentation.

Findings from OBSERVE:
- **Agenda is hardcoded** in the script (lines 275–295) despite a comment claiming it comes
  from `data/schedule.yaml`. It still contains the removed "Nebula" talk by Bleon Proko.
  Re-running alone would NOT fix it. The session data (`content/sessions/*.md`) is complete
  and structured (title, time, room, speakers), so the agenda can be made genuinely
  data-driven — which auto-fixes the stale slot.
- **Speaker tracks are hardcoded** (`TRACK_1`/`TRACK_2` sets) and the new speaker
  `mikkel-ole-romer` is in neither (would mis-default to Track 1 with a warning). Session
  rooms ("Store aud"=Track 1, "Lille aud"=Track 2) already encode this, so track can be
  derived from session data. `to-be-announced.md` → room "Store aud", speaker mikkel → Track 1.
- **Sponsors are absent** from the script entirely. `data/sponsors.yaml` has tiers, each with
  localized names and a `sponsors[]` list (name, url, logo, optional `darkBg`, description).
  `darkBg: true` (verified in main.css:488) = logo needs a white background tile.

Requested: extend the script to render sponsors + run it, with agenda/speakers current.
NOT requested: redesigning existing slide types, changing website, committing.

### Risks
- Making the agenda data-driven could regress a currently-working slide if session parsing
  is wrong. Mitigation: keep all rendering functions intact; change only the DATA source.
- incuba-logo.svg needs rasterization (rsvg-convert) — must handle gracefully if missing.
- No headless renderer (libreoffice) may be available for visual verify — fall back to
  parsing the saved pptx XML for required/forbidden strings.

## Criteria

Agenda (data-driven from schedule.yaml + sessions):
- [x] ISC-1: Agenda rows built from data/schedule.yaml at runtime
- [x] ISC-2: Session titles read from content/sessions/*.md frontmatter
- [x] ISC-3: Speaker display names resolved from speaker slug to title
- [x] ISC-4: Break and plenary rows render as full-width shared rows
- [x] ISC-5: 14:50 Track 1 cell shows "To Be Announced"
- [x] ISC-6: Room "Store aud" sessions map to Track 1 column
- [x] ISC-7: Room "Lille aud" sessions map to Track 2 column
- [x] ISC-A1: No "Nebula" text appears anywhere in the deck
- [x] ISC-A2: No "Bleon Proko" text appears anywhere in the deck

Speakers:
- [x] ISC-8: Speaker track derived from session room, not hardcoded sets
- [x] ISC-9: mikkel-ole-romer placed in Track 1
- [x] ISC-10: All 10 current speakers each get one bio slide
- [x] ISC-A3: No bio slide generated for removed bleon-proko

Sponsors:
- [x] ISC-11: load_sponsors() parses data/sponsors.yaml tiers
- [x] ISC-12: A sponsors slide is added to the deck
- [x] ISC-13: Sponsors grouped under their tier label
- [x] ISC-14: Sticker Mule name+logo appears on the sponsor slide
- [x] ISC-15: darkBg:true logos rendered on a white backing tile
- [x] ISC-16: Light logos rendered directly without a tile
- [x] ISC-17: Empty tier (Community Food Friends) omitted from slide
- [x] ISC-18: incuba SVG logo rasterized, or skipped with a warning

Run / verify:
- [x] ISC-19: Script runs to completion without exceptions
- [x] ISC-20: Output .pptx written with more slides than before
- [x] ISC-21: Saved pptx XML contains "Sticker Mule" and "To Be Announced"

## Decisions

- Made the agenda genuinely data-driven (schedule.yaml + sessions) rather than patching
  the hardcoded rows — the script's own comment claimed this was already the source. This
  auto-fixes the stale Nebula slot and prevents future drift.
- Derived speaker track from each session's `room` and REMOVED the legacy `TRACK_1/TRACK_2`
  hardcoded sets entirely (simplify/altitude finding) — they were already stale (listed the
  removed bleon-proko, missing the new mikkel-ole-romer) and were the same staleness trap.
- Sponsor slide renders logos (not text names) grouped under tier labels; `darkBg:true`
  logos get a white rounded tile, matching the website's `sponsor-logo--light-bg` CSS.
- Incuba's SVG is rasterized via the already-present `rsvg-convert`.

## Verification

- ISC-1..7,A1,A2 (agenda): re-ran script; rendered the agenda slide to PNG via qlmanage and
  visually confirmed all 9 rows match schedule.yaml; 14:50 Track 1 = "To Be Announced".
  `grep` of slide XML: Nebula count = 0, Bleon count = 0.
- ISC-8,9,10,A3 (speakers): build log "Track 1: 5, Track 2: 5" with NO track-warning →
  all 10 speakers (incl. new mikkel-ole-romer) placed via session room; removed bleon-proko
  produces no slide (no .md file). Removing legacy sets left output unchanged → confirms
  data-driven path covers everyone.
- ISC-11..18 (sponsors): rendered sponsor slide to PNG — 4 tier labels (Partners/Friends/
  Student Friends/Venue), empty Food Friends omitted. All 7 logos embedded (md5-verified vs
  source, incl. Sticker Mule = image8.png); darkBg tiles visible behind Aarhus Kommune,
  Sticker Mule, Incuba; light logos (Truesec, Tech Hub, Danske Bank, AU) direct.
- ISC-19,20,21 (run): script exits 0, `py_compile` OK, 16 slides written, XML contains
  "Sticker Mule" and "To Be Announced".
- Capability check: Skill("simplify") angles applied inline (spawn-restraint) → removed
  vestigial TRACK sets + unused `time` field; re-ran build, no regression.
