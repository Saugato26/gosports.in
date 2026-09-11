# Deploying betagsf.sreeb.dev

**Host:** Hostinger (Business plan), behind Hostinger's edge CDN (`server: hcdn`)
**Pipeline:** hPanel Git integration + GitHub webhook — a push to `main` is a deploy
**Build step:** none — the repository *is* the site

---

## 1. How a deploy works

hPanel Git clones this whole repository into the subdomain's web root and, on
each webhook call from GitHub, pulls `main`. There is no build and no file
filtering: **every tracked file lands in the web root.** `.htaccess` is what
decides which of those files the public can actually fetch.

## 2. What is served vs denied

| Path | Served? | Why |
|---|---|---|
| `*.html` (20 pages) | ✅ 200 | The site |
| `assets/css/`, `assets/js/`, `assets/img/` | ✅ 200 | The site |
| `robots.txt` | ✅ 200 | Must be readable to do its job (see §3) |
| `README.md`, `DEPLOY.md` | ⛔ 403 | Internal notes — README holds photo-provenance detail that should not be public |
| `.htaccess`, `.gitignore`, any dotfile | ⛔ 403 | Repository/server config |
| `LICENSE` (if ever added) | ⛔ 403 | Not part of the site |
| `.git/` and everything under it | ⛔ 404 | Created by the hPanel clone; exposing it would leak the full history |
| Directory listings | ⛔ | `Options -Indexes` |

The deny rule is a `FilesMatch` on the file name: `(^\.|\.md$|^LICENSE$)`.
**Adding a file?** Anything ending `.md` or starting with `.` is automatically
hidden; anything else you commit is public. If you add another internal file
type (notes, `.txt` drafts, source images), extend the pattern — and re-check it
against `git ls-files` so it still matches none of the site files.

## 3. Keeping the beta out of search engines — three layers

| Layer | Where | Covers |
|---|---|---|
| `robots.txt` → `Disallow: /` | repo root | Tells compliant crawlers not to fetch anything |
| `<meta name="robots" content="noindex, nofollow">` | all 20 pages | Pages, if a crawler fetches them anyway |
| `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` | `.htaccess` | Every response — including images and CSS, which meta tags can't cover |

Known limitation: `Disallow` blocks **crawling**, not **indexing**. A crawler
that obeys it never fetches a page, so never sees the `noindex` tag or header —
the bare URL can still appear in results if something public links to it. For
an unlinked beta this is acceptable; HTTP basic auth is the only airtight option.

**When the site goes to production, all three must be removed** — including the
meta tag on every page.

## 4. Caching — and when to purge the CDN

Set in `.htaccess`:

| Type | Browser cache |
|---|---|
| HTML | none (`access plus 0 seconds`) — a deploy is visible on next load |
| CSS, JS | 1 day |
| JPEG, PNG, SVG | 7 days |

Hostinger's CDN does **not** edge-cache HTML (`x-hcdn-cache-status: DYNAMIC`),
but it **does** cache CSS, JS and images at the edge. So after a deploy:

- HTML changes show immediately.
- **CSS, JS or image changes may not.** Purge the CDN from the site's CDN page
  in hPanel (Flush cache). Do this before concluding a deploy failed.
- `styles.css` and `main.js` are not fingerprinted, so returning visitors may
  also hold a stale copy in their browser for up to a day.
- Images are treated as immutable-by-name. To replace a photo, give the new
  file a new name rather than overwriting the old one.

HTTPS and the http→https redirect are handled at the CDN edge and are
deliberately **not** repeated in `.htaccess` (doing so behind the CDN risks a
redirect loop).

## 5. First-time setup (or re-connecting)

1. **The web root must be empty.** hPanel's Git clone refuses a non-empty
   directory. Anything there is reproducible from this repo, so delete it.
2. hPanel → Advanced → GIT → Create repository:
   - Repository: `https://github.com/Saugato26/gosports.in.git`
   - Branch: `main`
   - Directory: the subdomain's document root
   - The repo is public, so no deploy key is needed.
3. Deploy, then copy the **auto-deployment webhook URL** from the same page.
4. GitHub → repo Settings → Webhooks → Add webhook: paste the URL, content type
   `application/json`, "Just the push event", Active. (Requires repo admin.)

`.htaccess` must be on `main` **before** the first deploy — otherwise that
deploy publishes `README.md`.

## 6. Checking a deploy

```sh
for p in / /README.md /DEPLOY.md /.git/config /robots.txt; do
  printf '%-14s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' https://betagsf.sreeb.dev$p)"
done
curl -sI https://betagsf.sreeb.dev/ | grep -i x-robots-tag
```

Expected: `/` 200 · `README.md` 403 · `DEPLOY.md` 403 · `.git/config` 403 or
404 · `robots.txt` 200 · `X-Robots-Tag` present.
