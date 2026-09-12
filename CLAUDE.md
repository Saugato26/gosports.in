# GoSports Foundation beta site: working standards

Static HTML/CSS/JS, no build step, no dependencies. Live beta: https://betagsf.sreeb.dev (noindex).
Background lives elsewhere; read it before larger changes:
- `README.md`: site structure, content and image provenance, design notes
- `DEPLOY.md`: hosting, security layers, caching (section 4)
- `handover.html`: current open items and sign-offs for the content manager

## Content and facts

- Never invent people, donors, partners, quotes, numbers or awards. Everything must trace to the
  FY 2025–26 Annual Report, the vendor content doc, gosports.in, or a public source you checked.
- Verify every external link says what the page claims. An award links to a page that names
  GoSports as the winner; a LinkedIn link is confirmed to be the right person (name plus GoSports
  or a matching career history). Never guess or construct a URL. No source found means no link,
  and say so to the user.
- Bios of real people use only sourced facts. Titles are checked against gosports.in. Facts from
  weaker sources (ZoomInfo, RocketReach) are named as such in a beta note, and each person signs
  off before launch.
- Official copy (e.g. the film script from the YouTube description) goes in verbatim. Flag a
  possible typo to the user; don't silently fix it.
- Anything that needs confirming before launch gets a `<div class="note"><b>Beta note:</b> …</div>`
  next to it, and a line on `handover.html` where relevant.
- Prefer keeping visitors on the site: partner logos link to the programme that partner funds
  (see the funders page), not to the partner's social profiles.

## Design and front-end

- Brand tokens live in `assets/css/styles.css` `:root`: `--clay` #C71B23, `--ink` #101619, Satoshi
  (`--font-display`), IBM Plex Mono for eyebrows and labels. Don't add new colours or typefaces.
- Reuse existing patterns before inventing new ones: trustee/board card (photo, title, LinkedIn,
  bio), `.card`, `.logo-wall`, `.award`, `.note`, `.video-embed`. Match the surrounding markup,
  including its inline-style habits.
- Hover-only effects go inside `@media (hover:hover) and (pointer:fine)`, so phones get the
  full-colour default. Honour `prefers-reduced-motion`. Every link gets a `:focus-visible` state.
- Only things that are links should look clickable (lift, colour-on-hover). A linked tile is
  clickable across its whole area. External links use `target="_blank" rel="noopener"`.
- No third-party scripts on page load. Embeds are click-to-play (YouTube via youtube-nocookie,
  see `.video-embed` in `main.js`).
- Images carry `width`/`height`, `loading="lazy"`, `decoding="async"`, and real alt text
  (`alt=""` when the image is decorative or the text next to it already says the same).

## Verify before calling it done

- Serve locally: `python3 -m http.server 8765`. Opening the file directly skips the stylesheet.
- Look at the result. A headless Chrome screenshot is the reliable way here:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1280,8200 --virtual-time-budget=4000 --screenshot=out.png http://localhost:8765/<page>.html`
  then crop with `sips --cropOffset <y> <x> -c <h> <w> out.png`. Also check 375px width for
  horizontal overflow.
- After a push, confirm the GitHub Actions run "Deploy betagsf.sreeb.dev" passed and the change is
  on the live URL (`curl` it). An SSH timeout to Hostinger is transient: re-run the job.
- If the user sees an old design, `curl` the live page before assuming a bug. It's usually a
  browser tab that hasn't been reloaded (Cmd+Shift+R).

## Caching and deploy

- A push to `main` deploys (rsync over SSH). The workflow stamps the commit SHA onto every
  link to a file in `assets/css/` or `assets/js/`, so never bump `?v=` by hand, and new CSS/JS
  files are covered as long as they live in those folders and are linked from the HTML.
- HTML, CSS and JS are `no-cache`; images are cached for 1 hour. Don't change this without
  reading DEPLOY.md section 4. To swap an image instantly, use a new filename or clear the
  Hostinger cache (hPanel, or the Hostinger API's clear-website-cache for betagsf.sreeb.dev).
- Every page has a link-preview (Open Graph) card. After adding a page or changing a page's
  headline or title, add or update its entry in `PAGES` in `tools/og/build.py` and run
  `python3 tools/og/build.py <page>`. It renders `assets/img/og/<page>.jpg` and rewrites the
  tags between `<!-- og:start -->` and `<!-- og:end -->`; don't hand-edit that block. When the
  site moves to its production domain, change `BASE_URL` there and re-run for all pages.
- A new repo-only file (docs, scripts) must be added to the rsync excludes in
  `.github/workflows/deploy.yml`. `.htaccess` also denies `*.md` and dotfiles as a second layer.

## Git

- Other Claude sessions often work in this repo at the same time. Run `git status` first, stage
  only the files you changed, and leave other sessions' uncommitted work alone.
- Commit and push when the user asks or approves. Commit messages say what changed and why.
