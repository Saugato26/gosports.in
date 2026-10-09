#!/usr/bin/env python3
"""Render every programme-<slug>.html from one shared layout and a content file.

    python3 tools/programmes/build.py            # all programmes
    python3 tools/programmes/build.py ubhar      # just programme-ubhar.html

Content lives in tools/programmes/content/<slug>.json. A new programme is a new
content file plus an entry in tools/og/build.py's PAGES (then run that script
for the link-preview card) and a card on programmes.html. No new page design.

The layout, top to bottom. Every section except the hero and the closing cards
is optional: leave its key out of the JSON and the section is omitted, so a
programme never shows a filler section. Section backgrounds alternate
automatically. Any section can take an "id" for in-page links.

  hero          title, description, breadcrumb, h1, lede          (required)
  summary       eyebrow?, paragraphs, image?, chips?, logo?, supporter?
  partnership   eyebrow, heading, paragraphs, quote {quote, name, role}
  numbers       eyebrow?, heading?, items [{value, label}], footnote?
  academies     eyebrow, heading, intro?, items [{tag, name, meta, text}], beta_note?
  pillars       eyebrow, heading, items [{title, text}]
  story         eyebrow?, heading?, image {src, alt, width, height, shape,
                caption?}, image_comment?, name, role, paragraphs
  testimonials  eyebrow?, heading?, items [{quote, name, role}]
  gallery       eyebrow, heading, images [{src, alt, width, height}]
  next          [{title, text, link? {href, label}}]   (defaults to NEXT)

Values are HTML fragments, copied verbatim from the approved copy: entities
(&ndash;) and inline tags (<b>, <i>) are kept as written. Eyebrows and headings
marked "?" fall back to DEFAULTS; set one to null to drop it.

The page's Open Graph block (between og:start and og:end) is kept from the
existing file; tools/og/build.py owns it.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CONTENT = os.path.join(HERE, "content")
sys.path.insert(0, os.path.join(ROOT, "tools", "nav"))
import build as nav  # noqa: E402  (tools/nav/build.py)

DEFAULTS = {
    "summary": {"eyebrow": "Executive summary"},
    "numbers": {"eyebrow": "FY 2025–26 snapshot", "heading": "The programme in numbers"},
    "story": {"eyebrow": "Athlete impact story", "heading": "From the field"},
    "testimonials": {"eyebrow": "In their words", "heading": "Beneficiary testimonials"},
}
NEXT = [
    {"title": "Explore more", "text": "See our full portfolio of initiatives across Indian sport.",
     "link": {"href": "programmes.html", "label": "Our programmes"}},
    {"title": "Fund this work", "text": "See who funds programmes like this one, and how.",
     "link": {"href": "funders.html", "label": "Our funders"}},
    {"title": "Partner with us", "text": "Work with us to build impactful, high-performance systems.",
     "link": {"href": "get-involved.html", "label": "Get involved"}},
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — GoSports Foundation</title>
<meta name="description" content="{description}">
{og}
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=satoshi@400,500,600,700,900&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/css/styles.css?v=2026091211">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/icons/icon-192.png">
<link rel="apple-touch-icon" href="assets/img/icons/icon-180.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#C71B23">
<meta name="robots" content="noindex, nofollow">
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>

{header}

<main id="main-content">
"""

FOOT = """
</main>

<section class="footer-cta">
  <div class="container footer-cta-row">
    <div>
      <h2>Become a changemaker.</h2>
      <p>Build ecosystems of excellence. Drive meaningful change.</p>
      <span class="hashtag">#ChampioningExcellence</span>
    </div>
    <a href="get-involved.html" class="btn" style="background:#fff;color:var(--clay);">Get involved</a>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="nav-logo"><img src="assets/img/gallery/brand-white-logo.svg" alt="GoSports Foundation" width="132" height="44"></div>
        <p class="small mt-1" style="color:#8C9092;">A system-level sports development organisation building research-backed frameworks that champion excellence across Indian sport. Est. 2008.</p>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="programmes.html">Programmes</a></li>
          <li><a href="funders.html">Our Funders</a></li>
          <li><a href="sapa-centre.html">SAPA Centre</a></li>
          <li><a href="performance-institute.html">Performance Institute</a></li>
          <li><a href="get-involved.html">Get Involved</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="gallery.html">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h2>Get Involved</h2>
        <ul>
          <li><a href="get-involved.html#volunteer">Volunteer</a></li>
          <li><a href="get-involved.html#donate">Donate</a></li>
          <li><a href="get-involved.html#partner">Partner</a></li>
          <li><a href="careers.html">Careers</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="mailto:info@gosports.in">info@gosports.in</a></li>
        </ul>
      </div>
      <div>
        <h2>Follow</h2>
        <ul>
          <li><a href="https://www.instagram.com/gosportsvoices/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.linkedin.com/company/gosports-foundation" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="https://www.youtube.com/user/GoSportsVoices" target="_blank" rel="noopener">YouTube</a></li>
          <li><a href="https://x.com/GoSportsVoices" target="_blank" rel="noopener">X</a></li>
          <li><a href="https://www.facebook.com/GoSportsFoundation/" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year></span> GoSports Foundation. Beta site — content in review.</span>
      <span>#ChampioningExcellence</span>
    </div>
  </div>
</footer>

<script src="assets/js/main.js?v=2026091211"></script>
</body>
</html>
"""

NUM_STYLE = "display:block;font-size:1.8rem;color:var(--ink);font-family:var(--font-mono);"
P_STYLE = "color:var(--ink-soft);"


def img(i, extra=""):
    return (f'<img src="{i["src"]}" alt="{i["alt"]}" width="{i["width"]}" height="{i["height"]}"'
            f'{extra} loading="lazy" decoding="async">')


def figure(i):
    shape = {"square": "media square", "wide": "media wide"}.get(i.get("shape"), "media")
    cap = f'<figcaption>{i["caption"]}</figcaption>' if i.get("caption") else ""
    return f'<figure class="{shape}">{img(i)}{cap}</figure>'


def head(sec, intro=None):
    """Eyebrow + heading (+ intro) in the site's .section-head pattern."""
    parts = []
    if sec.get("eyebrow"):
        parts.append(f'<span class="eyebrow">{sec["eyebrow"]}</span>')
    if sec.get("heading"):
        parts.append(f'<h2>{sec["heading"]}</h2>')
    if intro:
        parts.append(f"<p>{intro}</p>")
    if not parts:
        return ""
    return '      <div class="section-head">\n' + "".join(f"        {p}\n" for p in parts) + "      </div>\n"


def quote(q, small=False):
    style = ' style="font-size:1.05rem;"' if small else ""
    return (f'        <div class="testimonial">\n'
            f'          <blockquote{style}>{q["quote"]}</blockquote>\n'
            f'          <cite><b>{q["name"]}</b>{q["role"]}</cite>\n'
            f'        </div>\n')


def s_summary(s):
    paras = "".join(f'        <p class="mt-1" style="{P_STYLE}">{p}</p>\n' for p in s["paragraphs"])
    chips = ""
    if s.get("chips"):
        chips = ('        <div class="grid grid-2 mt-2" style="gap:0.75rem;">\n'
                 + "".join(f'          <span class="partner-chip">{c}</span>\n' for c in s["chips"])
                 + "        </div>\n")
    logo = ""
    if s.get("logo"):
        lg = s["logo"]
        logo = "        " + img(lg, f' style="max-width:{lg["max_width"]};height:auto;margin:1.5rem 0 0;"') + "\n"
    sup = ""
    if s.get("supporter"):
        sup = ('        <div class="note" style="border-color:var(--ink-soft);background:var(--paper-dim);'
               f'color:var(--ink-soft);">{s["supporter"]}</div>\n')
    eyebrow = f'        <span class="eyebrow">{s["eyebrow"]}</span>\n' if s.get("eyebrow") else ""
    body = eyebrow + paras + chips + logo + sup
    if s.get("image"):
        return ('    <div class="container grid grid-2" style="align-items:center;gap:3rem;">\n'
                f'      {figure(s["image"])}\n'
                f'      <div>\n{body}      </div>\n'
                '    </div>\n')
    return f'    <div class="container">\n      <div>\n{body}      </div>\n    </div>\n'


def s_partnership(s):
    paras = "".join(f'        <p class="mt-2" style="{P_STYLE}">{p}</p>\n' for p in s["paragraphs"])
    return ('    <div class="container grid grid-2" style="gap:3rem;">\n'
            '      <div>\n'
            f'        <span class="eyebrow">{s["eyebrow"]}</span>\n'
            f'        <h2 style="font-size:clamp(1.7rem,3vw,2.2rem);">{s["heading"]}</h2>\n'
            f'{paras}'
            '      </div>\n'
            + quote(s["quote"]) +
            '    </div>\n')


def s_numbers(s):
    cards = "".join(
        f'        <div class="card" style="text-align:center;"><span class="num" style="{NUM_STYLE}">'
        f'{i["value"]}</span><span class="small">{i["label"]}</span></div>\n' for i in s["items"])
    foot = f'      <p class="small mt-2">{s["footnote"]}</p>\n' if s.get("footnote") else ""
    return (f'    <div class="container">\n{head(s)}'
            f'      <div class="grid grid-4">\n{cards}      </div>\n{foot}    </div>\n')


def s_academies(s):
    cards = "".join(
        f'        <div class="prog-card"><span class="tag">{i["tag"]}</span><h3>{i["name"]}</h3>'
        f'<p class="small" style="font-family:var(--font-mono);font-size:0.75rem;">{i["meta"]}</p>'
        f'<p class="small">{i["text"]}</p></div>\n' for i in s["items"])
    note = f'      <div class="note beta mt-2"><b>Beta note:</b> {s["beta_note"]}</div>\n' if s.get("beta_note") else ""
    comment = f'      <!-- {s["comment"]} -->\n' if s.get("comment") else ""
    return (f'    <div class="container">\n{comment}{head(s, s.get("intro"))}'
            f'      <div class="grid grid-4">\n{cards}      </div>\n{note}    </div>\n')


def s_pillars(s):
    cards = "".join(
        f'        <div class="card"><span class="num">{n:02d}</span><h3>{i["title"]}</h3><p>{i["text"]}</p></div>\n'
        for n, i in enumerate(s["items"], 1))
    return f'    <div class="container">\n{head(s)}      <div class="grid grid-4">\n{cards}      </div>\n    </div>\n'


def s_story(s):
    comment = f'        <!-- {s["image_comment"]} -->\n' if s.get("image_comment") else ""
    paras = "".join(f'          <p class="mt-1">{p}</p>\n' for p in s["paragraphs"])
    return (f'    <div class="container">\n{head(s)}'
            '      <div class="grid grid-2" style="gap:2rem;align-items:start;">\n'
            f'{comment}        {figure(s["image"])}\n'
            '        <div>\n'
            f'          <h3 style="font-size:1.3rem;">{s["name"]} <span class="small" style="font-weight:400;">— {s["role"]}</span></h3>\n'
            f'{paras}'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n')


def s_testimonials(s):
    three = len(s["items"]) >= 3
    items = "".join(quote(q, small=three) for q in s["items"])
    return (f'    <div class="container">\n{head(s)}'
            f'      <div class="grid {"grid-3" if three else "grid-2"}">\n{items}      </div>\n    </div>\n')


def s_gallery(s):
    figs = "".join(f'        <figure class="media square">{img(i)}</figure>\n' for i in s["images"])
    return f'    <div class="container">\n{head(s)}      <div class="grid grid-4">\n{figs}      </div>\n    </div>\n'


def s_next(cards):
    out = []
    for c in cards:
        link = ""
        if c.get("link"):
            link = f'\n        <a href="{c["link"]["href"]}" class="btn btn-ghost btn-sm mt-1">{c["link"]["label"]}</a>'
        out.append(f'      <div class="card">\n        <h3>{c["title"]}</h3>\n        <p>{c["text"]}</p>{link}\n      </div>\n')
    return '    <div class="container grid grid-3">\n' + "".join(out) + "    </div>\n"


SECTIONS = [("summary", s_summary), ("partnership", s_partnership), ("numbers", s_numbers),
            ("academies", s_academies), ("pillars", s_pillars), ("story", s_story),
            ("testimonials", s_testimonials), ("gallery", s_gallery)]

OG_RE = re.compile(r"<!-- og:start.*?<!-- og:end -->", re.S)


def render(slug, d, existing=""):
    page = f"programme-{slug}.html"
    m = OG_RE.search(existing)
    og = m.group(0) if m else "<!-- og:start (run tools/og/build.py) -->\n<!-- og:end -->"
    out = [HEAD.format(title=d["title"], description=d["description"], og=og, header=nav.render(page))]
    out.append('  <section class="page-hero">\n    <div class="container">\n'
               f'      <span class="breadcrumb"><a href="programmes.html" style="color:var(--gold);">PROGRAMMES</a> / {d["breadcrumb"]}</span>\n'
               f'      <h1>{d["h1"]}</h1>\n'
               f'      <p class="lede">{d["lede"]}</p>\n'
               '    </div>\n  </section>\n')
    alt = False
    bodies = []
    for key, fn in SECTIONS:
        if key in d:
            sec = {**DEFAULTS.get(key, {}), **d[key]}
            bodies.append((key, sec.get("id"), fn(sec)))
    bodies.append(("next", None, s_next(d.get("next", NEXT))))
    for key, id_, body in bodies:
        cls = "section section-alt" if alt else "section"
        anchor = f' id="{id_}"' if id_ else ""
        out.append(f'\n  <!-- {key.upper()} -->\n  <section class="{cls}"{anchor}>\n{body}  </section>\n')
        alt = not alt
    out.append(FOOT)
    return "".join(out)


def build(slug):
    d = json.load(open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8"))
    path = os.path.join(ROOT, f"programme-{slug}.html")
    existing = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    html = render(slug, d, existing)
    if html != existing:
        open(path, "w", encoding="utf-8").write(html)
        print(f"wrote programme-{slug}.html")
    if not OG_RE.search(existing):
        print(f"  new page: add 'programme-{slug}' to PAGES in tools/og/build.py and run it")


if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(CONTENT) if f.endswith(".json"))
    for s in slugs:
        build(s.removeprefix("programme-"))
