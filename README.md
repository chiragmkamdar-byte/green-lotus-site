# Green Lotus Spices — static site

A plain HTML/CSS rebuild of greenlotusvn.com (originally a Wix site), ready to deploy on Vercel.

## What's here

- `index.html` — Home
- `our-spices.html` — Product overview
- `products/*.html` — 7 individual product pages (Black Pepper, White Pepper, Star Anise, Cassia, Cashews, Dried Red Chilli, Desiccated Coconut)
- `about-us.html`, `contact-us.html`
- `vercel.json` — caching config (optional, safe to delete)

No build step, no dependencies — it's static HTML that Vercel serves as-is. All CSS is inlined directly in each page.

## Deploy to Vercel

**Option A — Vercel dashboard (no CLI needed)**
1. This repo is already on GitHub.
2. Go to vercel.com → **Add New... → Project**.
3. Import this repo (chiragmkamdar-byte/green-lotus-site).
4. Framework preset: **Other** (it's plain static HTML — no build command, no output directory needed).
5. Click **Deploy**.

**Option B — Vercel CLI**
```
npm install -g vercel
git clone https://github.com/chiragmkamdar-byte/green-lotus-site.git
cd green-lotus-site
vercel        # deploy a preview
vercel --prod # deploy to production
```

## Connect your domain

Once deployed, in the Vercel project go to **Settings → Domains** and add `greenlotusvn.com` and `www.greenlotusvn.com`. Vercel will give you DNS records (usually an A record or CNAME) to add wherever the domain is currently registered/managed. Once DNS propagates, Vercel issues an SSL certificate automatically.

Note: your domain is likely still pointed at Wix's nameservers/DNS today. You'll need access to wherever the domain itself is registered (not just the Wix site editor) to repoint it.

## About the contact/enquiry forms

The original Wix forms submitted to Wix's own backend. Since this is now static hosting, the forms here are wired to `mailto:` links as a simple fallback — clicking Submit will open the visitor's email client instead of silently posting data. For real inline form handling (submissions land in your inbox or a spreadsheet without opening email), wire the `<form>` `action` in each page to a service like Formspree, Getform, or a small Vercel serverless function.

## Images

Images are currently referenced directly from Wix's media CDN (`static.wixstatic.com`) so nothing had to be re-uploaded. These URLs are stable, but if you ever want full independence from Wix, download the images and swap the `src` paths to local files (e.g. `/img/black-pepper.jpg`).
