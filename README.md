# GoSports Foundation — Beta Website

**Status:** Beta / internal review
**Prepared for:** GoSports Foundation leadership
**Source content:** vendor content & wireframe doc (Home, About Us, Programmes, Programme Pages, Get Involved — plus Careers, tone guidelines, and the 100x Accelerator narrative)

---

## 1. What this is

This is a working beta of the GoSports Foundation website, built from the vendor's existing content and restructured around two things at once: the **six questions** every visitor is really asking, and the **seven audiences** who ask them.

**The six questions (the site's backbone):**
1. Who are we?
2. What do we do?
3. How do we do it?
4. Who has funded us to do this?
5. What are we doing next?
6. Come work for us.

**The seven audiences (who's asking):**
Potential athlete managers, CSR professionals, athletes, potential ecosystem partners (universities/equipment manufacturers/government), philanthropists/foundations, job applicants, and researchers.

The vendor draft had strong content but was organised the way an internal team thinks about the organisation, not the way a first-time visitor — from any of the seven groups above — finds what they need. This beta keeps almost all of the vendor's copy, but sequences the homepage as a clean six-beat story, and adds a dedicated page for the one question the original draft answered weakest: **who's funded us.**

This is a **static HTML/CSS/JS site** — no build step, no server required. It opens directly in a browser and is ready to drop into a GitHub repo and serve via GitHub Pages (or any static host).

---

## 1a. What changed in this pass (11 Sep 2026)

The site went from "structurally complete but unillustrated" to "illustrated", and one blocking
mobile bug was fixed along the way.

**Photography — 18 of 28 placeholders filled.** 23 assets extracted from the FY 2025–26 Annual
Report (Version 6), cropped and optimised to 2.2 MB total. Six athletes are named on the evidence of
their own story pages; the rest are honestly labelled as representative. Full provenance and the 10
deliberately-open slots are in section 3a. Pages that previously had zero images — the homepage,
Gear for Gold, all 11 athlete stories, Get Involved, SAPA Centre — now have them.

**Fixed: the mobile menu was completely broken.** On every one of the 20 pages, at any width
≤900px, the nav panel collapsed to a 32px strip showing only "Home" — it also overlapped the logo,
and tapping the toggle did nothing. About Us, Programmes, Our Funders, Get Involved and Careers were
**unreachable on a phone**.

Cause: `.site-header` uses `backdrop-filter`, which makes it the *containing block* for its
`position: fixed` children. So `inset: 64px 0 0 0` on `.nav-links` resolved against the 64px-tall
header instead of the viewport, and `translateY(-110%)` moved the panel by only 35px. Fixed in
`assets/css/styles.css` by sizing and translating the panel in viewport units
(`height: calc(100dvh - 64px)`, `translateY(-110vh)`), plus `visibility` toggling so the closed menu
isn't focusable. Full-width tap targets restored via `.nav-links li{ width:100% }`.

**Regression tested** at 375 / 768 / 1280px across all 20 pages: zero horizontal overflow, all 30
images resolve, no console errors, mobile menu opens and closes correctly.

**Known issue, not yet fixed:** `assets/css/styles.css:6` loads Google Fonts via CSS `@import`,
which serialises the page load (HTML → CSS → font CSS → font files). Moving it to
`<link rel="preconnect">` + `<link>` in each `<head>` would measurably improve first paint, but it
touches all 20 files — worth doing as its own change.

---

## 2. Site map

| Page | File | Built from |
|---|---|---|
| Home | `index.html` | Vendor content + annual report data |
| About Us | `about.html` | Vendor content + real Trustees/Board (photos &amp; bios) from the FY 2025–26 Annual Report |
| Programmes | `programmes.html` | All 12 real programmes from the Annual Report, each linking to its own page |
| 12 programme detail pages | `programme-*.html` | Executive summary, FY snapshot stats, one athlete impact story, and beneficiary testimonials — all pulled directly from the FY 2025–26 Annual Report |
| Our Funders | `funders.html` | Real Foundation Partner logos (extracted from the report), every programme-specific corporate/foundation funder, and federation/government partners |
| SAPA Centre | `sapa-centre.html` | New — built from sports-society.org, GoSports' incubated research &amp; policy arm |
| The Performance Institute | `performance-institute.html` | New — built from an internal Axis Bank x GoSports Foundation grant proposal deck. See the note in section 3 below before this goes anywhere public. |
| Get Involved | `get-involved.html` | Vendor content, restructured around CSR / ecosystem partners / philanthropists, with tiered giving |
| Careers | `careers.html` | Vendor content |

**The 12 real programmes**, each with its own page: Gear for Gold (Infosys Foundation), Para Champions Programme (IndusInd Bank, since 2015), Rahul Dravid Athlete Mentorship Programme, Aditya Birla Capital Sports Scholarship for Women, Samarth Para Sports Programme (Hyundai Motor India Foundation), Murugappa Rising Talent Sports Scholarship (AMM Foundation), UBHAR Programme (Tata Trusts), Equal Hue Cricket Excellence Programme, CM Athlete Coaching &amp; Empowerment Scheme (Govt. of Arunachal Pradesh), RCB Cares Sports Development Programme, GoSports Long-Term Athlete Development Programme, and Tayyari Jeet Ki (Mondelez India, launched 2026).

**On the homepage**, the story runs: Hero → **Find your lane** (the 7-audience wayfinder) → Who We Are → What We Do → How We Do It → Our Impact → Testimonials → Who's Funded Us → What's Next → Achievements → Come Work For Us → footer.

**The "Find your lane" section** is the main navigation aid for the seven audiences — each is a direct link to the page and section built for them:

| Audience | Where they land |
|---|---|
| Athlete managers / academies | Programmes → Gear for Gold model |
| CSR professionals | Get Involved → Partner section |
| Athletes | Programmes |
| Ecosystem partners (universities, equipment, govt) | Get Involved → Partner section |
| Philanthropists / foundations | Get Involved → Donate section |
| Job applicants | Careers |
| Researchers | About → Research section |

---

## 3. What's real content vs. what's a placeholder

This beta now pulls real data from two source documents: the original vendor content/wireframe doc, and GoSports' **FY 2025–26 Annual Report** (`GSF_ANNUAL_REPORT_-_VERSION_4_.pdf`). Here's what's real, what's extracted, and what's still a placeholder:

- **All 12 programme pages** (`programme-*.html`): executive summaries, FY 2025–26 snapshot stats, one athlete impact story, and 1–2 beneficiary testimonials per programme — all real, pulled directly from the Annual Report. Athlete photography is now in place on 11 of the 12 pages — 6 of those are the named athlete themselves, 5 are sport-matched representative shots. See section 3a.
- **Trustees &amp; Board Members** (`about.html`): six real people (Nandan Kamath, Abhishek Laxminarayan, Thomas Ollapally, Unmish Parthasarathi, Meghana Narayan, Deepthi Bopaiah) with real bios and **real photos**, cropped directly from the Annual Report.
- **Executive Leadership** (`about.html`): Saugato Banerjee and Sonali Anna Philip's names and titles come from a dense staff-directory page in the report — worth a quick confirmation with HR, since titles were harder to parse cleanly from that layout than the Trustee bios were. John Gloster's title (Director of Sports Science) is carried over from the original vendor content, corroborated by a testimonial mentioning him in this report, but not independently re-confirmed.
- **Foundation Partner logos** (`funders.html`): six real logos (Rainmatter by Zerodha, Nandi Housing, LawNK, Dr. Syed Ahmed Memorial Charitable Trust, Fusion Finance, MVS) cropped directly from the report. They're report-quality crops, not brand-supplied source files — ask each partner for their current logo asset before this goes live anywhere public.
- **Our Funders page**: every corporate, foundation, and federation/government partner named is real, collated from the Annual Report — including which programme each one funds. This replaces the earlier, thinner placeholder list.
- **SAPA Centre page** (`sapa-centre.html`): new. Built from sports-society.org (the Sports and Society Accelerator's own site), since GoSports' Annual Report references the SAPA Centre and SAPA Stack Framework without fully explaining them. Confirmed: SSA was co-founded by Nandan Kamath (GoSports' own Managing Trustee).
- **Photography** (athletes in action, academies, events): **18 of the original 28 image placeholders are now filled** with real photography extracted from the FY 2025–26 Annual Report (see section 3a below for the full provenance table and the 10 that remain open).
- **Careers:** no open roles were listed in any source document, so the page invites CVs by email instead of showing fake postings.
- **Contact emails** (`partnerships@gosports.in`, `volunteer@gosports.in`, `giving@gosports.in`, `careers@gosports.in`): still invented for this beta to make CTAs functional — **confirm or replace with real inboxes before this goes further than internal review.**
- **Giving tiers on Get Involved** (`#donate`): the six amounts match the live donation page exactly; the "what this funds" line next to each is illustrative copy, not a confirmed cost.
- **"Sustaining the System" section on Our Funders** (`#sustaining`): a **proposed** new giving category modelled on peer foundations — not something GoSports currently runs. Flagged in-page as a recommendation.
- **"What's Next" section on the homepage:** SAPA Centre is now real and linked; Thought Leadership and Alumni Network remain as noted in the original vendor content. The Performance Institute now has its own full page and a featured spot here.

---

## 3a. Image provenance — read this before the site goes public

All photography was extracted from **`GSF ANNUAL REPORT - VERSION 6.pdf`** (90 pages, the newest
version — note the rest of this README's *copy* came from Version 4). Images were cropped to the
slot's aspect ratio and resized down to fit; **nothing was upscaled**, so a few are soft (flagged
below). Assets live in `assets/img/`.

**Attribution method.** The Annual Report places each athlete's photo on the same page as that
athlete's own written story. Where the photo came from the named athlete's story page *and* the
sport matches the slot, the athlete is named in the `alt` text. Everywhere else the `alt` text
describes the scene generically and the markup carries an HTML comment marked
`REPRESENTATIVE IMAGE`. **No photo asserts an identity that isn't evidenced.**

### Named athletes (6) — photo from that athlete's own story page

| Page | Asset | Athlete | Evidence |
|---|---|---|---|
| `programme-ehcep.html` | `athlete-tanmayee-behera.jpg` | Tanmayee Behera, Cricket | Report p51, her story page; wearing Odisha kit (she plays for Odisha) |
| `programme-gltadp.html` | `athlete-aneesh-gowda.jpg` | Aneesh Gowda, Swimming | Report p56, his story page |
| `programme-mrtss.html` | `athlete-mantra-lokesh.jpg` | Mantra Lokesh, Para Athletics | Report p61, his story page |
| `programme-rdamp.html` | `athlete-raja-muthupandi.jpg` | Raja Muthupandi, Weightlifting | Report p71, his story page |
| `programme-samarth.html` | `athlete-yash-kumar.jpg` | Yash Kumar, Para Canoe | Report p77, his story page |
| `programme-tayyari-jeet-ki.html` | `athlete-mishka-choudhary.jpg` | Mishka Choudhary, Sports Climbing | Report p82, her story page |

### Representative images (5) — sport-matched, athlete NOT identified

Each is flagged in-page with an HTML comment. Swap for a photo of the actual athlete when one exists.

| Page | Asset | Note |
|---|---|---|
| `programme-abcssw.html` | `sport-badminton-doubles.jpg` | Doubles pair in India colours, from the ABCSSW section opener. Source is only 450×450 — **soft**, replace when possible. |
| `programme-pcp.html` | `sport-swimming.jpg` | Swimming, not para swimming — the report had no para-swimming photo. |
| `programme-rcb-cares.html` | `sport-athletics-highjump.jpg` | From the RCB Cares section opener; athletics, correct programme. |
| `programme-ubhar.html` | `academy-cohort.jpg` | Cohort photo standing in for the Bhoir Gymkhana academy. |
| `programme-gear-for-gold.html` | `gfg-gallery-1…4.jpg` | 4-up "Capturing impact" gallery: badminton, weightlifting, swimming, sports-science testing. |

### Other images placed

`home-ecosystem.jpg` (homepage, para javelin — the slot was a video, so the caption says the film is
still in production), `volunteer-event.jpg` (Get Involved), `sapa-convening.jpg` (SAPA Centre),
`gfg-academy.jpg` (Gear for Gold intro).

### Still open — 10 placeholders left, deliberately

These were left as `.ph-media` blocks because **no honest asset exists** in the source material.
Substituting an athlete's face for a named executive, or another facility for the CSE campus, would
have been a fabrication:

| Slot | What's needed |
|---|---|
| `about.html` ×3 | Headshots: Saugato Banerjee, Sonali Anna Philip, John Gloster |
| `performance-institute.html:319` | John Gloster headshot (same asset as above) |
| `performance-institute.html:66` | Architectural **render** of the PI laboratory building |
| `performance-institute.html:202` | Photo of the Centre for Sports Excellence campus, Bengaluru |
| `careers.html` ×3 | Staff portraits — **and** the three testimonial quotes, which are still "Testimonial to be added" |
| `programme-cm-aces.html:69` | Biri Takar, Para-Badminton — no para-badminton photo in the report |

### Unused assets held in the repo

Four extracted images are committed but not yet placed on a page, because the honest home for them
isn't obvious. All four are web-ready:

- `athlete-ekta-bhyan.jpg` — para club throw, Kobe 2024. Her name is legible on the bib, so this must
  only ever be used to represent **Ekta Bhyan**. It was *not* used for the para-badminton slot.
- `cohort-equal-hue.jpg` — cohort photo whose banner reads "Equal Hue Cricket Excellence Programme",
  so it belongs on EHCEP material, not Gear for Gold.
- `science-testing.jpg` — 1600×900 sports-science testing session. The obvious home is the
  Performance Institute page, but both of its open slots ask for specific things (a building render
  and the CSE campus), so it would have been mislabelled there. A square crop of this image *is* in
  use as `gfg-gallery-4.jpg`.
- `team-group.jpg` — 1600×900 photo of the full Foundation team. Would suit an About page "our team"
  section, which doesn't exist yet.

The two programme logos extracted from the report (`logo-ubhar.png`, `logo-tayyari-jeet-ki.png`) *are*
now placed, on their respective programme pages above the funder note.

### Known caveats

- These are **crops out of a PDF**, not original photography. Ask the comms team for the original
  files before any public launch — several are below ideal resolution (`athlete-tanmayee-behera.jpg`
  is 407×407, `sport-badminton-doubles.jpg` 450×450).
- **Model release / consent:** these images were cleared for the Annual Report. Confirm the same
  consent covers website use, especially for the minors visible in the cohort photos.

---

### ⚠️ A flag on The Performance Institute page

This page (`performance-institute.html`) is built from an internal grant proposal deck for a ₹40 Cr, 4-year partnership between Axis Bank and GoSports Foundation — a deck marked **"Axis Bank Document Classification | Confidential"** on every slide, and still going through Axis Bank's internal approval process at the time it was written ("Agenda 4(c) — Approval for New Proposals"). A search of the Drive also turned up a **draft, unpublished press release** for this partnership with unfilled placeholders (`[Date]`, `[Designation]`, `[to be added]`), suggesting the partnership had not been publicly announced as of that draft.

Per direction from GoSports leadership, this page has been built in full — including the budget breakdown, governance structure, and a list of **potential** (not yet confirmed) experts under discussion for the institute — with the understanding that GoSports will manage disclosure risk and confirm timing with Axis Bank before this goes live anywhere public. If that changes, pull the budget table, the potential-experts section, and the Axis Bank naming before publishing.

---

## 4. Design notes

- **Palette:** deep navy (`#12172B`), track-clay red (`#C1442E`), medal gold (`#E8A62A`) on a cool paper-white background — grounded in athletics (track surface, stadium lights, medal) rather than a generic corporate-nonprofit look.
- **Typography:** Big Shoulders Display (condensed, scoreboard/signage character) for headings, IBM Plex Sans for body text, IBM Plex Mono for stats and labels.
- **Signature idea:** the "concentric rings" motif on the homepage hero (athlete at the centre, surrounded by coaches/family, academies/systems, and policy/partners) is a direct visual translation of GoSports' own language — "we build the ecosystem around the athlete." The "Find your lane" audience section on the homepage echoes the same idea using running-track lanes.
- **Fundraising section (Get Involved + Our Funders):** restructured after reviewing the live gosports.in donation flow (a bare amount-picker with no context) against [The Majurity Trust's "Who We Are" page](https://www.majurity.sg/who-we-are-majurity/), which explains what different levels of giving fund, names real people behind its major gifts, and keeps a running donor wall. GoSports' beta now gives each donation amount a concrete "what this funds" line, proposes an unrestricted "Sustaining the System" giving tier, and adds a donor wall built to grow. All of it uses only real names already in the source content — nothing here invents a donor or board member that doesn't exist.
- **Photo &amp; logo extraction:** Trustee/Board photos and Foundation Partner logos in this beta were cropped directly from page renders of the Annual Report PDF (not separately supplied image files). They're usable for an internal beta review, but swap in proper source files — official headshots, brand-supplied logo packs — before anything here goes to a public audience.
- All interactive elements (accordion, tabs, mobile nav) are plain JavaScript, no dependencies.
- Fonts load from Google Fonts via CDN — this requires an internet connection when the site is viewed (normal for any deployed site; won't work in a fully offline preview).

---

## 5. How to preview it

**Locally, no setup:** open `index.html` directly in a browser.

**With a local server** (recommended, so relative links and anchors behave exactly like production):
```bash
cd gosports-beta
python3 -m http.server 8000
# then visit http://localhost:8000
```

---

## 6. How to publish it on GitHub

1. Copy everything in this folder into your GitHub repo (keep `index.html` at the repo root, or inside a `/docs` folder if you'd rather keep it separate from other code).
2. Commit and push.
3. In the repo's **Settings → Pages**, set the source to the branch/folder containing `index.html`.
4. GitHub will publish it at `https://<your-org>.github.io/<repo-name>/`.

No build tools, no `npm install`, no framework — it's ready as-is.

---

## 7. Suggested next steps

1. **Confirm the contact emails** in section 3 above, or send real ones.
2. **Send real photography/video** for athletes, academies, and events — the only real photos in this beta are the six Trustee/Board headshots and six partner logos, all cropped from the Annual Report PDF.
3. **Decide on final headlines** — the source doc offered several headline options per page; this beta picked one per page, but it's worth a quick leadership review before these are locked in.
4. **Confirm Executive Leadership titles** — Saugato Banerjee, Sonali Anna Philip, and John Gloster's roles were pieced together from a dense staff-directory layout; a quick HR check would firm these up.
5. **Get proper logo files** from the six Foundation Partners and get real photo/video assets — the report crops work for internal review but shouldn't go external.
6. **Confirm the SAPA Centre framing** — this beta describes it as GoSports' incubated research arm (via shared leadership with SSA); check that framing is exactly how GoSports wants the relationship described publicly.
7. **Decide the second new page** — SAPA Centre is built; if there's a second page you had in mind, let me know what it is and I'll build it the same way.

---

*This README was generated alongside the beta build to keep the reasoning behind each decision visible for the team — update or trim it as the project matures.*
