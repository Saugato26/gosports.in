#!/usr/bin/env python3
"""Rewrite the site header (logo, main nav, Donate button) on every public page
from one definition, so the nav never drifts between pages.

    python3 tools/nav/build.py           # every public page
    python3 tools/nav/build.py about     # just about.html

Replaces everything from <header class="site-header"> to </header>. The nav
marks the current page with aria-current="page" and its section parent with
aria-current="true". Safe to re-run. handover.html and checklist.html are
internal and deliberately left alone.

Edit NAV below to change the menu; tools/programmes/build.py imports render().
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Top-level items, left to right. A "children" list makes the item a dropdown
# parent; "section" lists the pages that count as inside it (for the current-
# section marker) without appearing in the menu.
NAV = [
    {"label": "About us", "href": "about.html", "id": "about",
     "children": [("About GoSports", "about.html"),
                  ("SAPA Centre", "sapa-centre.html"),
                  ("Careers", "careers.html")]},
    {"label": "Programmes", "href": "programmes.html",
     "section": ["performance-institute.html"], "section_prefix": "programme-"},
    {"label": "Get involved", "href": "get-involved.html", "id": "involved",
     "children": [("Partner with us", "funders.html"),
                  ("Ways to get involved", "get-involved.html")]},
]
# The donate page doesn't exist yet; the button points at the Donate section
# of get-involved.html until it does.
DONATE_HREF = "get-involved.html#donate"
SKIP = {"handover.html", "checklist.html"}

LOGO = ('<a href="index.html" class="nav-logo" aria-label="GoSports Foundation — home">'
        '<img src="assets/img/gallery/brand-logo-black.webp" alt="GoSports Foundation" width="264" height="88"></a>')


def _in_section(item, page):
    pages = {item["href"]} | {h for _, h in item.get("children", [])} | set(item.get("section", []))
    return page in pages or (item.get("section_prefix") and page.startswith(item["section_prefix"]))


def _cur(href, page):
    return ' aria-current="page"' if href == page else ""


def render(page):
    """Return the <header> block for `page` (a filename like 'about.html')."""
    out = ['<header class="site-header">',
           '  <nav class="nav container" aria-label="Main">',
           "    " + LOGO,
           '    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="site-navigation"><span></span><span></span><span></span></button>',
           '    <ul class="nav-links" id="site-navigation">']
    for item in NAV:
        inside = _in_section(item, page)
        own = item["href"] == page and not item.get("children")
        cur = ' aria-current="page"' if own else (' aria-current="true"' if inside else "")
        if "children" in item:
            sub = f'nav-sub-{item["id"]}'
            out.append('      <li class="nav-group">')
            out.append(f'        <a href="{item["href"]}"{cur}>{html.escape(item["label"])}</a>'
                       f'<button class="nav-sub-toggle" aria-expanded="false" aria-controls="{sub}" '
                       f'aria-label="Show {html.escape(item["label"])} pages"></button>')
            out.append(f'        <ul class="nav-sub" id="{sub}">')
            for label, href in item["children"]:
                out.append(f'          <li><a href="{href}"{_cur(href, page)}>{html.escape(label)}</a></li>')
            out.append('        </ul>')
            out.append('      </li>')
        else:
            out.append(f'      <li><a href="{item["href"]}"{cur}>{html.escape(item["label"])}</a></li>')
    out += [f'      <li class="nav-menu-cta"><a href="{DONATE_HREF}" class="btn btn-primary">Donate</a></li>',
            '    </ul>',
            '    <div class="nav-cta">',
            f'      <a href="{DONATE_HREF}" class="btn btn-primary btn-sm">Donate</a>',
            '    </div>',
            '  </nav>',
            '</header>']
    return "\n".join(out)


HEADER_RE = re.compile(r'<header class="site-header">.*?</header>', re.S)


def apply(page):
    path = os.path.join(ROOT, page)
    src = open(path, encoding="utf-8").read()
    new, n = HEADER_RE.subn(lambda _: render(page), src, count=1)
    if n != 1:
        sys.exit(f"{page}: no site header found")
    if new != src:
        open(path, "w", encoding="utf-8").write(new)
        print(f"updated {page}")


def pages():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and f not in SKIP)


if __name__ == "__main__":
    targets = [a if a.endswith(".html") else a + ".html" for a in sys.argv[1:]] or pages()
    for p in targets:
        apply(p)
