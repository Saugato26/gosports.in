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
server: `.git/`, `.github/`, `.gitignore`, `README.md`, `DEPLOY.md`. `.htaccess`
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
| `.git/` and everything under it | ⛔ 404 | Not shipped. `RedirectMatch` also 404s it, for the stale clone left by the old setup |
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
