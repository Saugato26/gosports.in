# Deploying betagsf.sreeb.dev

**Host:** Hostinger (Business plan), behind Hostinger's edge CDN (`server: hcdn`)
**Pipeline:** GitHub Actions → `rsync` over SSH — a push to `main` is a deploy
**Build step:** none — the repository *is* the site

---

## 1. How a deploy works

`.github/workflows/deploy.yml` runs on every push to `main`. It checks the repo
out on a GitHub runner and `rsync`s it to the web root over SSH, with
`--delete` so the server is an exact mirror of `main`. There is no build step.

Repo-only files are **excluded from the transfer**, so they never exist on the
server: `.git/`, `.github/`, `.gitignore`, `README.md`, `DEPLOY.md`,
`fetch-live-images.sh`, and `assets/img/live/` (the 27 MB raw archive pulled from
gosports.in — the optimised versions in `assets/img/gallery/` are what ships). `.htaccess`
denies the same set as a second layer, in case one ever arrives by another route
(a manual `git pull` on the box, a File Manager upload).

Two defences, deliberately: exclusion means the file isn't there (404); the
`.htaccess` rule means that even if it is, it can't be fetched (403).

**Credentials:** repo secret `SSH_PRIVATE_KEY` holds an ed25519 key whose public
half is registered in hPanel → Advanced → SSH Access → SSH keys. Optional secret
`SSH_KNOWN_HOSTS` pins the server host key; without it the workflow trusts the
key on first use and logs a warning.

> ⚠️ Hostinger SSH keys are **account-wide**, not per-site. This deploy key can
> reach every site on the hosting account, not just betagsf. hPanel offers no
> `command=` restriction, so treat the secret accordingly.

## 2. What is served vs denied

| Path | Served? | Why |
|---|---|---|
| `*.html` (20 pages) | ✅ 200 | The site |
| `assets/css/`, `assets/js/`, `assets/img/` | ✅ 200 | The site |
| `robots.txt` | ✅ 200 | Must be readable to do its job (see §3) |
| `README.md`, `DEPLOY.md` | ⛔ 404 | Not shipped (rsync excludes them). `.htaccess` would also 403 them |
| `.htaccess`, any dotfile | ⛔ 403 | Server config — `.htaccess` must ship, so it is denied rather than excluded |
| `.gitignore` | ⛔ 404 | Not shipped |
| `LICENSE` (if ever added) | ⛔ 403 | Not part of the site |
| `.git/`, `.github/` and everything under them | ⛔ 404 | Not shipped. `RedirectMatch 404 /\.git(hub)?(/\|$)` also 404s them — `.github/workflows/deploy.yml` names the server IP, port and user, and `FilesMatch` can't catch it because it matches on basename |
| Directory listings | ⛔ | `Options -Indexes` |

The deny rule is a `FilesMatch` on the file name: `(^\.|\.md$|\.sh$|^LICENSE$)`.
**Adding a file?** Anything ending `.md` or starting with `.` is automatically
hidden; anything else you commit is public. If you add another internal file
type (notes, `.txt` drafts, source images), extend the pattern — and re-check it
against `git ls-files` so it still matches none of the site files.

## 3. Keeping the beta out of search engines — three layers

| Layer | Where | Covers |
|---|---|---|
| `robots.txt` → `Disallow: /` for every crawler except named link-preview bots | repo root | Tells compliant crawlers (Google, Bing, AI crawlers) not to fetch anything. LinkedIn, X, Facebook/WhatsApp, Slack and Telegram preview bots are allowed so shared links show the preview card; they build previews, not a search index |
| `<meta name="robots" content="noindex, nofollow">` | every page | Pages, if a crawler fetches them anyway |
| `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` | `.htaccess` | Every response — including images and CSS, which meta tags can't cover |

> ⚠️ **Basic auth is currently commented out in `.htaccess`** so the beta can be
> browsed without a password. Layers 1-3 below are all that is active, and
> layer 3 does not reach images. Re-enable before sharing the URL.

**Layer 4, and the only airtight one: HTTP basic auth.** `.htaccess` requires a
valid user for every request. A 401 cannot be indexed at all.

Two limitations made the first three layers insufficient on their own:

- `Disallow` blocks **crawling**, not **indexing**. A crawler that obeys it
  never fetches the page, so never sees the `noindex` tag or header — the bare
  URL can still appear in results if anything public links to it.
- **`X-Robots-Tag` does not reach images on this host.** Measured, not assumed:
  HTML, CSS, JS and `.txt` all carry the header, but `.jpg` and `.png` carry
  neither it nor `nosniff`, on cache MISS as well as HIT — so it is the origin,
  not the CDN. LiteSpeed serves image types on a static fast path that skips
  `mod_headers`. (`mod_expires` *does* apply to them — images return
  `max-age=604800` as configured — so `.htaccess` is being read; only the
  header table is skipped.) The directives now use `Header always set`, which
  may or may not change this; **it has not been verified**. Basic auth closes
  the gap regardless.

**When the site goes to production, all three must be removed** — including the
meta tag on every page.

## 4. Caching — and when to purge the CDN

Set in `.htaccess`. The aim is that a deploy is visible on the next page load
without anyone remembering a manual step:

| Type | Browser and CDN cache |
|---|---|
| HTML, CSS, JS, `.webmanifest`, `.txt` | `no-cache`: a copy may be kept, but it is checked with the server on every load (an unchanged file is a tiny 304) |
| Images (JPEG, PNG, WebP, SVG, ICO …) | 1 hour |

- **CSS/JS versions are stamped automatically.** Before uploading, the deploy
  workflow rewrites every link to a file in `assets/css/` or `assets/js/`
  (with or without an existing `?v=`) to `?v=<commit short SHA>`. Every
  deploy gives stylesheets and scripts new URLs, so even a copy a browser
  cached under an older, longer rule is never used again. The `?v=` numbers
  in the repo are placeholders and never need bumping by hand.
  The workflow's verify step fails if the live homepage doesn't link the
  new version, or if HTML/CSS/JS stop sending `no-cache`.
- **Replacing an image under the same filename** shows within the hour.
  Hostinger's CDN also keeps images at the edge for up to that hour; for an
  instant swap, give the new file a new name, or clear the cache in hPanel
  (Websites → betagsf.sreeb.dev → Cache / CDN → Flush cache).
- Hostinger's CDN does not edge-cache HTML (`x-hcdn-cache-status: DYNAMIC`).
- A browser tab left open (or restored) from before a change can still show
  the old page until it is reloaded; if it looks very old, hard-reload
  (Cmd+Shift+R). No server setting can reach a copy the browser never asks
  about.
- When the site is public and stable, image caching can be raised again (e.g.
  7 days) for speed — at that point, rename replaced images rather than
  overwriting them.

HTTPS and the http→https redirect are handled at the CDN edge and are
deliberately **not** repeated in `.htaccess` (doing so behind the CDN risks a
redirect loop).

## 5. First-time setup (or re-connecting)

**`.htpasswd` must exist before `.htaccess` reaches the server**, or every
request 500s. Create it first, over SSH:

```sh
ssh -p 65002 u306132917@145.79.58.193 \
  "printf '%s\\n' 'gsfbeta:\$apr1\$SvMR8ivr\$Y9NEDbsxTpK3w7ZSveWaD.' \
   > domains/betagsf.sreeb.dev/.htpasswd && chmod 644 domains/betagsf.sreeb.dev/.htpasswd"
```

**Mode must be 644, not 600.** LiteSpeed's worker does not run as `u306132917`,
so a 600 file is unreadable to it — and it reports that as **401, not 500**, so
it looks exactly like a wrong password. If correct credentials are rejected,
check the mode before you touch the hash. The file is still not web-reachable:
it sits above the web root, and `/.htpasswd`, `/../.htpasswd` and the
percent-encoded traversal all return 403.

It sits one level above the web root, so it is not web-reachable at all — and
it is deliberately not in the repo, since the repo is public.

To change the password later: `htpasswd -c .htpasswd gsfbeta` on any machine
with Apache tools, or `openssl passwd -apr1` to generate the hash by hand.

1. Generate a keypair: `ssh-keygen -t ed25519 -C gh-actions-deploy-betagsf -f ./gsf_deploy -N ""`
2. hPanel → Advanced → SSH Access → **SSH keys** → add `gsf_deploy.pub`.
3. GitHub → repo Settings → Secrets and variables → Actions → New secret:
   - `SSH_PRIVATE_KEY` = the full contents of `gsf_deploy` (including the
     BEGIN/END lines).
   - `SSH_KNOWN_HOSTS` (recommended) = output of
     `ssh-keyscan -p 65002 145.79.58.193`.
   Both require repo admin on `Saugato26/gosports.in`.
4. Push to `main`, or run the workflow manually from the Actions tab.

The workflow verifies the live site itself and fails the run if any check is
wrong, so a red build means the deploy did not land as intended.

### Manual deploy, no CI

The web root is also a git checkout, so the server can pull directly:

```sh
ssh -p 65002 u306132917@145.79.58.193 \
  'cd domains/betagsf.sreeb.dev/public_html && \
   git fetch --depth=1 origin main && git reset --hard FETCH_HEAD && git clean -fd'
```

Note this ships *every* tracked file, including `README.md` and `DEPLOY.md` —
they are then 403 by `.htaccess` rather than absent. Don't mix the two routes
casually; `rsync --delete` will remove what the pull added.

### Routes that did not work

- **hPanel → Advanced → GIT** is now a GitHub App OAuth install, not the old
  "repository URL + branch + directory + webhook URL" form. There is no webhook
  URL to copy any more.
- **Hostinger cron jobs** were tried as a polling deploy (`*/5` git fetch/reset).
  The jobs registered and appeared in hPanel but never executed — no output, no
  `FETCH_HEAD`, not even a bare `touch` landing. Don't rely on account cron here
  without proving it fires first.

## 6. Checking a deploy

```sh
for p in / /README.md /DEPLOY.md /.git/config /robots.txt; do
  printf '%-14s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' https://betagsf.sreeb.dev$p)"
done
curl -sI https://betagsf.sreeb.dev/ | grep -i x-robots-tag
```

Expected after a CI deploy: `/` 200 · `README.md` 404 · `DEPLOY.md` 404 ·
`.git/config` 404 · `robots.txt` 200 · `X-Robots-Tag` present.

After a manual `git pull` deploy instead: `README.md` and `DEPLOY.md` are 403
rather than 404, because they are present but denied.
