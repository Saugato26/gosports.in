#!/usr/bin/env python3
"""Build the Open Graph (link preview) card for every page, and keep each page's
OG/Twitter meta tags in sync.

    python3 tools/og/build.py            # all pages
    python3 tools/og/build.py about      # just about.html

Needs Google Chrome (headless) and macOS `sips`. Writes assets/img/og/<page>.jpg
(1200x630) and rewrites the block between <!-- og:start --> and <!-- og:end -->
in each page's <head>. Safe to re-run. Add new pages to PAGES below.

BASE_URL is the site's public origin. Change it once when the site moves to its
production domain and re-run; social apps require absolute image URLs.
"""
import html, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_URL = "https://betagsf.sreeb.dev"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_DIR = os.path.join(ROOT, "assets", "img", "og")

# page: (eyebrow, headline, photo relative to assets/img or None, CSS object-position)
PAGES = {
    "index":                 ("GoSports Foundation", "Behind every athlete is a team. Help us build theirs.", "home-ecosystem.jpg", "center 35%"),
    "about":                 ("About us", "Championing excellence in Indian sport.", "team-group.jpg", "center"),
    "programmes":            ("Programmes", "Empowering athletes, academies & communities.", "gallery/hero-sprint-start.webp", "center"),
    "funders":               ("Our funders", "Who's funded this work.", "gallery/photo-programme-launch.webp", "center"),
    "get-involved":          ("Get involved", "Champion change in sport.", "volunteer-event.jpg", "center 30%"),
    "careers":               ("Careers", "Build systems. Champion excellence.", "gallery/hero-office.webp", "center"),
    "gallery":               ("Gallery", "Every image we have.", "gallery/hero-athlete-mosaic.webp", "center"),
    "performance-institute": ("What we're building next", "The Performance Institute.", "science-testing.jpg", "center"),
    "sapa-centre":           ("SAPA Centre", "The research engine behind the ecosystem.", "sapa-convening.jpg", "center"),
    "programme-abcssw":      ("Programme", "Aditya Birla Capital Sports Scholarship for Women", "sport-badminton-doubles.jpg", "center"),
    "programme-cm-aces":     ("Programme", "Chief Minister's Athlete Coaching and Empowerment Scheme", "gallery/photo-cm-aces-cohort.webp", "center"),
    "programme-ehcep":       ("Programme", "Equal Hue Cricket Excellence Programme", "cohort-equal-hue.jpg", "center"),
    "programme-gear-for-gold": ("Programme", "Gear for Gold", "gfg-academy.jpg", "center"),
    "programme-gltadp":      ("Programme", "GoSports Long-Term Athlete Development Programme", "athlete-aneesh-gowda.jpg", "center 30%"),
    "programme-mrtss":       ("Programme", "Murugappa Rising Talent Sports Scholarship", "athlete-mantra-lokesh.jpg", "center 30%"),
    "programme-pcp":         ("Programme", "Para Champions Programme", "sport-swimming-v2.jpg", "center"),
    "programme-rcb-cares":   ("Programme", "The RCB Cares Sports Development Programme", "sport-athletics-highjump.jpg", "center"),
    "programme-rdamp":       ("Programme", "Rahul Dravid Athlete Mentorship Programme", "gallery/hero-rahul-dravid-portrait.webp", "center 25%"),
    "programme-samarth":     ("Programme", "Samarth Para Sports Programme", "athlete-yash-kumar-v2.jpg", "center 30%"),
    "programme-tayyari-jeet-ki": ("Programme", "Tayyari Jeet Ki", "athlete-mishka-choudhary.jpg", "center 30%"),
    "programme-ubhar":       ("Programme", "UBHAR Programme", "academy-cohort.jpg", "center"),
    "checklist":             ("Internal", "Master website checklist", None, ""),
    "handover":              ("Internal", "Website handover", None, ""),
}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=satoshi@500,700,900&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
  *{box-sizing:border-box;margin:0}
  html,body{width:1200px;height:630px;overflow:hidden;background:#101619}
  .card{position:relative;width:1200px;height:630px;display:flex;font-family:'Satoshi',sans-serif;color:#fff}
  .text{position:relative;flex:1;padding:60px 64px 56px;display:flex;flex-direction:column;overflow:hidden}
  .logo{height:46px;width:auto;align-self:flex-start}
  .mid{flex:1;display:flex;flex-direction:column;justify-content:center;padding:28px 0 16px}
  .eyebrow{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;letter-spacing:.16em;text-transform:uppercase;color:#E8A62A;display:flex;align-items:center;gap:14px;margin-bottom:22px}
  .eyebrow::before{content:'';width:34px;height:2px;background:#C71B23}
  h1{font-weight:900;font-size:{size}px;line-height:1.06;letter-spacing:-.01em;flex:none}
  .tag{font-family:'IBM Plex Mono',monospace;font-size:16px;letter-spacing:.06em;color:#8C9092}
  .rings{display:none;position:absolute;pointer-events:none}
  .photo{position:relative;width:500px;height:630px;flex:none}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo::before{content:'';position:absolute;left:0;top:0;bottom:0;width:10px;background:#C71B23;z-index:1}
  .nophoto .text{padding-right:360px}
  .nophoto .rings{display:block;right:40px;top:105px;width:420px;height:420px}
</style></head><body>
<div class="card {cls}">
  <div class="text">
    <svg class="rings" viewBox="0 0 400 400" aria-hidden="true">
      <circle cx="200" cy="200" r="185" fill="none" stroke="rgba(244,245,240,0.12)" stroke-width="1.5"/>
      <circle cx="200" cy="200" r="140" fill="none" stroke="rgba(244,245,240,0.18)" stroke-width="1.5"/>
      <circle cx="200" cy="200" r="95" fill="none" stroke="#E8A62A" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>
      <circle cx="200" cy="200" r="40" fill="#C71B23"/>
    </svg>
    <img class="logo" src="{logo}" alt="">
    <div class="mid">
      <div class="eyebrow">{eyebrow}</div>
      <h1 id="h">{headline}</h1>
    </div>
    <div class="tag">#ChampioningExcellence</div>
  </div>
  {photo}
</div>
</body></html>"""


def headline_size(text):
    # Big for short headlines, stepping down so long programme names stay within ~4 lines.
    n = len(text)
    return 76 if n <= 26 else 66 if n <= 42 else 58 if n <= 58 else 52


def render(page, eyebrow, headline, photo, pos, tmp):
    img_root = os.path.join(ROOT, "assets", "img")
    photo_html = ""
    if photo:
        photo_html = ('<div class="photo"><img src="file://%s" style="object-position:%s" alt=""></div>'
                      % (os.path.join(img_root, photo), pos))
    doc = (TEMPLATE
           .replace("{cls}", "" if photo else "nophoto")
           .replace("{logo}", "file://" + os.path.join(img_root, "gallery", "brand-white-logo.svg"))
           .replace("{eyebrow}", html.escape(eyebrow))
           .replace("{headline}", html.escape(headline))
           .replace("{photo}", photo_html)
           .replace("{size}", str(headline_size(headline))))
    src = os.path.join(tmp, page + ".html")
    png = os.path.join(tmp, page + ".png")
    with open(src, "w") as f:
        f.write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=1",
                    "--window-size=1200,630", "--virtual-time-budget=5000",
                    "--screenshot=" + png, "file://" + src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out = os.path.join(OUT_DIR, page + ".jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", png, "--out", out],
                   check=True, stdout=subprocess.DEVNULL)
    return out


def meta_block(page, eyebrow, headline, html_src):
    title = re.search(r"<title>(.*?)</title>", html_src, re.S).group(1).strip()
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html_src, re.S)
    desc = desc_m.group(1) if desc_m else ""
    og_title = title if page == "index" else re.sub(r"\s+—\s+GoSports Foundation.*$", "", title)
    url = BASE_URL + "/" + ("" if page == "index" else page + ".html")
    image = "%s/assets/img/og/%s.jpg" % (BASE_URL, page)
    alt = html.escape("GoSports Foundation: " + headline, quote=True)
    return "\n".join([
        "<!-- og:start (generated by tools/og/build.py; edit PAGES there, not here) -->",
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="GoSports Foundation">',
        '<meta property="og:locale" content="en_IN">',
        '<meta property="og:title" content="%s">' % og_title,
        '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:image" content="%s">' % image,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="%s">' % alt,
        '<meta name="twitter:card" content="summary_large_image">',
        "<!-- og:end -->",
    ])


def update_meta(page, eyebrow, headline):
    path = os.path.join(ROOT, page + ".html")
    s = open(path).read()
    block = meta_block(page, eyebrow, headline, s)
    if "<!-- og:start" in s:
        s = re.sub(r"<!-- og:start.*?<!-- og:end -->", lambda m: block, s, flags=re.S)
    else:
        # right after the meta description (or <title> if a page has none)
        anchor = re.search(r'<meta name="description"[^>]*>\n', s) or re.search(r"</title>\n", s)
        s = s[:anchor.end()] + block + "\n" + s[anchor.end():]
    open(path, "w").write(s)


def main():
    only = sys.argv[1:]
    missing = [p for p in only if p not in PAGES]
    if missing:
        sys.exit("Unknown page(s): %s. Add them to PAGES first." % ", ".join(missing))
    unlisted = sorted(f[:-5] for f in os.listdir(ROOT) if f.endswith(".html") and f[:-5] not in PAGES)
    if unlisted and not only:
        print("warning: no OG card defined for: " + ", ".join(unlisted))
    os.makedirs(OUT_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for page in (only or PAGES):
            eyebrow, headline, photo, pos = PAGES[page]
            out = render(page, eyebrow, headline, photo, pos, tmp)
            update_meta(page, eyebrow, headline)
            print("ok  %-28s %s (%d KB)" % (page, os.path.relpath(out, ROOT), os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()
