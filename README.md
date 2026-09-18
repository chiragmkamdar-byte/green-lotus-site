# Green Lotus Spices — greenlotusvn.com

A plain HTML/CSS static site deployed on Vercel. No framework, no dependencies.

## How the site is built

Every `.html` file is **generated** by `tools/build.py`. Edit the content in
`tools/build.py` (page copy) or `tools/products.py` (product data and
specification tables), then run:

```
python3 tools/build.py
```

and commit the regenerated files. Editing the `.html` files by hand works, but
the next build overwrites those edits — so change the source, not the output.

```
tools/build.py       page templates, shared header/footer, site copy
tools/products.py    the seven products: grades, specs, photography, SEO
assets/site.css      all styling (previously duplicated inline in 11 pages)
assets/site.js       navigation, logo, form submission
img/logo-data.js     the logo as a data URI
```

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home |
| `our-spices.html` | Product range |
| `products/*.html` | Seven product pages with full specification tables |
| `certifications.html` | Certifications, testing and export documents |
| `packaging-shipping.html` | Packing, container quantities, Incoterms, transit |
| `about-us.html` | Company, numbers, sourcing, team |
| `contact-us.html` | Contact details and the enquiry form |
| `sitemap.xml`, `robots.txt` | Generated for search engines |

## Before this goes live

**1. Fill in the placeholders.** Anything the site does not yet know renders as
a highlighted `[bracket]`. Find them all with:

```
grep -c 'class="todo"' *.html products/*.html
```

They are all defined in one place — the `F = { ... }` dictionary near the top of
`tools/build.py`. Replace each `todo("...")` with the real value and rebuild.

**2. Check every specification figure.** The tables in `tools/products.py` are
standard Vietnamese export grades taken from common trade practice, **not Green
Lotus lab data**. A published specification is a commitment to the buyer, so
check each figure against your own certificates of analysis before merging.

**3. Wire up the forms.** The old forms posted to `mailto:`, which most browsers
ignore and phones drop entirely — enquiries were being lost. Create a free
endpoint at [Formspree](https://formspree.io) or [Web3Forms](https://web3forms.com)
and paste the URL into `window.GL_FORM_ENDPOINT` at the top of `assets/site.js`.
Until you do, the forms fall back to opening a mail client, exactly as before.

**4. Redirect the bare domain.** The site answers on both `greenlotusvn.com` and
`www.greenlotusvn.com`. Pick one as canonical and 301 the other in Vercel
(Settings → Domains), or Google splits the ranking between two copies of every
page. The `<link rel="canonical">` tags currently point at the `www` version.

## Deploy

Vercel builds from this repo automatically on push to `main`. For a preview,
push a branch and open a pull request — Vercel comments with a preview URL.

## Images

Images are still served from Wix's media CDN (`static.wixstatic.com`), left over
from the original site. They work, but for independence from Wix, download them
into `img/` and update the URLs in `tools/products.py`.

Worth replacing eventually with your own photography: the warehouse, the
processing line, staff at work, containers loading. Stock farm imagery does
nothing for an importer; a photo of your actual facility does.
