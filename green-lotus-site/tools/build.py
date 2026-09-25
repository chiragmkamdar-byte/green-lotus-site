#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for greenlotusvn.com.

Every .html file in this repository is produced by this script. Edit the
content here, run `python3 tools/build.py` from the repository root, and commit
the regenerated files. Editing the .html files directly works too, but the next
build will overwrite those edits.

Placeholders: anything wrapped in `todo()` renders as a highlighted [bracket]
on the page. Search the built site for `class="todo"` — none should remain when
this goes live.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from products import PRODUCTS, PRODUCTS_BY_SLUG, RANGE_CARDS  # noqa: E402

RANGE_IMG = {slug: (img, alt) for slug, img, alt, _ in RANGE_CARDS}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.greenlotusvn.com"

SALES_EMAIL = "sales@greenlotusvn.com"
ADMIN_EMAIL = "admin@greenlotusvn.com"


def todo(text):
    """A fact we do not have yet. Renders highlighted so it cannot ship unnoticed."""
    return '<span class="todo" title="Replace this before publishing">%s</span>' % text


# --------------------------------------------------------------------------
# Company facts used across the site.
#
# Growing regions are the established Vietnamese production areas for each
# crop, not a statement about specific farms — confirm they match where Green
# Lotus actually buys before this goes live.
#
# Deliberately not published yet: registered numbers, addresses, volumes,
# headcount, MOQ, lead time, port of loading, Incoterms, packing weights and
# certifications. Add them here when you want them on the site.
# --------------------------------------------------------------------------
F = {
    "phone": "+84 889 004 111",
    "phone_href": "tel:+84889004111",
    "city": "Ho Chi Minh City",
    "founded": "2022",
    "company_name_full": "Green Lotus Spice Company Limited",
    "company_name_vn": "CÔNG TY TNHH GIA VỊ SEN XANH",
    "markets": "Taiwan, Europe, the UAE and the United States",
    "payment": "20% advance, balance 80% cash against documents by T/T",
    "provinces": "Dak Lak, Gia Lai, Dong Nai and Binh Phuoc",
    "cassia_provinces": "Yen Bai, Quang Nam and Thanh Hoa",
    "anise_provinces": "Lang Son and Cao Bang",
    "cashew_provinces": "Binh Phuoc and Dong Nai",
    "chilli_provinces": "the Mekong Delta and the central coast",
    "coconut_provinces": "Ben Tre and Tra Vinh",
}


def fmt(text):
    """Substitute {placeholders} without tripping over CSS braces."""
    def swap(match):
        key = match.group(1)
        return F.get(key, match.group(0))
    return re.sub(r"\{(\w+)\}", swap, text)


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

NAV_ITEMS = [
    ("index.html", "Home", "home"),
    ("our-spices.html", "Our Spices", "spices"),
    ("about-us.html", "About Us", "about"),
    ("contact-us.html", "Contact Us", "contact"),
]


def rel(depth, path):
    return ("../" * depth) + path


def utility_bar(depth):
    return fmt("""<div class="utility-bar">
  <div class="inner">
    <div class="util-left">Vietnamese spice exporter &mdash; quotes within one business day</div>
    <div class="util-right">
      <a href="{phone_href}">{phone}</a>
      <span class="sep">|</span>
      <a href="mailto:%s">%s</a>
    </div>
  </div>
</div>""" % (SALES_EMAIL, SALES_EMAIL))


def header(depth, active):
    dropdown = "\n".join(
        '            <li><a href="%s">%s</a></li>'
        % (rel(depth, "products/%s.html" % p["slug"]), p["nav"])
        for p in PRODUCTS
    )
    items = []
    for href, label, key in NAV_ITEMS:
        cls = ' class="active"' if key == active else ""
        if key == "spices":
            items.append(
                '        <li%s>\n'
                '          <a href="%s">%s</a>\n'
                '          <ul class="dropdown-menu">\n%s\n          </ul>\n'
                '        </li>' % (cls, rel(depth, href), label, dropdown)
            )
        else:
            items.append('        <li%s><a href="%s">%s</a></li>' % (cls, rel(depth, href), label))

    return """%s
<header class="site-header">
  <div class="nav-wrap">
    <a href="%s" class="logo"><img alt="Green Lotus Spices" class="js-logo"></a>
    <nav class="main-nav">
      <ul>
%s
      </ul>
    </nav>
    <div class="nav-right">
      <a href="%s" class="nav-cta">Request a quote</a>
      <button class="mobile-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>""" % (utility_bar(depth), rel(depth, "index.html"), "\n".join(items), rel(depth, "contact-us.html"))


def footer(depth):
    product_links = "\n".join(
        '        <li><a href="%s">%s</a></li>'
        % (rel(depth, "products/%s.html" % p["slug"]), p["nav"])
        for p in PRODUCTS
    )
    return fmt("""<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <div class="logo"><img alt="Green Lotus Spices" class="js-logo"></div>
      <p>Vietnamese spice exporter supplying pepper, cassia, star anise, cashews, dried chilli and desiccated coconut to large manufacturers and supermarkets worldwide.</p>
    </div>
    <div>
      <h4>Products</h4>
      <ul>
%s
      </ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="%s">About us</a></li>
        <li><a href="%s">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <p>{company_name_full}</p>
      <p>{city}, Vietnam</p>
      <p><a href="{phone_href}">{phone}</a></p>
      <p><a href="mailto:%s">%s</a></p>
    </div>
  </div>
  <div class="fine-print">&copy; 2026 Green Lotus Spices. All rights reserved.</div>
</footer>""" % (
        product_links,
        rel(depth, "about-us.html"),
        rel(depth, "contact-us.html"),
        SALES_EMAIL, SALES_EMAIL,
    ))


def page(path, title, description, body, depth=0, schema=None, active=""):
    canonical = "%s/%s" % (DOMAIN, path)
    schema_block = ""
    if schema:
        schema_block = '<script type="application/ld+json">\n%s\n</script>\n' % schema

    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s</title>
<meta name="description" content="%s" />
<link rel="canonical" href="%s" />
<meta property="og:type" content="website" />
<meta property="og:title" content="%s" />
<meta property="og:description" content="%s" />
<meta property="og:url" content="%s" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%s" />
%s</head>
<body>

%s

%s

%s

<script src="%s"></script>
<script src="%s"></script>
</body>
</html>
""" % (
        title, description, canonical, title, description, canonical,
        rel(depth, "assets/site.css"),
        schema_block,
        header(depth, active),
        body.strip(),
        footer(depth),
        rel(depth, "img/logo-data.js"),
        rel(depth, "assets/site.js"),
    )

    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as handle:
        handle.write(fmt(html))
    return path


# --------------------------------------------------------------------------
# Reusable blocks
# --------------------------------------------------------------------------

def spec_table(spec):
    head = "".join("<th>%s</th>" % h for h in spec["headers"])
    rows = "\n".join(
        "        <tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row)
        for row in spec["rows"]
    )
    return """<!-- REVIEW: these are standard Vietnamese export grades, not Green Lotus lab data.
     Check every figure against your own certificates of analysis before publishing. -->
<div class="table-wrap">
  <table class="spec">
    <caption>%s</caption>
    <thead><tr>%s</tr></thead>
    <tbody>
%s
    </tbody>
  </table>
</div>""" % (spec["caption"], head, rows)


def quote_form(depth, subject, product_default=""):
    options = "\n".join(
        '            <option%s>%s</option>'
        % (" selected" if p["slug"] == product_default else "", p["name"])
        for p in PRODUCTS
    )
    return fmt("""<form class="enquiry" id="enquiry" data-subject="%s" action="mailto:%s" method="post" enctype="text/plain">
      <h3>Request a quote</h3>
      <p class="lead-in">Tell us what you need and we will come back with a price, a specification sheet and samples within one business day.</p>
      <div class="form-row">
        <div><label for="q-name">Name</label><input type="text" id="q-name" name="Name" required /></div>
        <div><label for="q-company">Company</label><input type="text" id="q-company" name="Company" required /></div>
      </div>
      <div class="form-row">
        <div><label for="q-email">Email</label><input type="email" id="q-email" name="Email" required /></div>
        <div><label for="q-whatsapp">Phone / WhatsApp</label><input type="text" id="q-whatsapp" name="Phone" /></div>
      </div>
      <div class="form-row">
        <div>
          <label for="q-product">Product</label>
          <select id="q-product" name="Product">
%s
            <option>Other</option>
          </select>
        </div>
        <div><label for="q-grade">Grade or specification</label><input type="text" id="q-grade" name="Grade" placeholder="e.g. ASTA 570 g/l" /></div>
      </div>
      <div class="full-row">
        <label for="q-notes">Notes</label>
        <textarea id="q-notes" name="Notes" placeholder="Volume, destination, packing preference, certification requirements — anything that helps us quote"></textarea>
      </div>
      <button type="submit" class="btn" style="background:var(--green);color:#fff">Send enquiry</button>
      <p class="form-note">We reply to every enquiry within one business day. Your details are used to quote your requirement and nothing else.</p>
      <div class="form-status" role="status"></div>
    </form>""" % (subject, SALES_EMAIL, options))


def cta_band(depth, heading="Ready to price your requirement?",
             text="Send us the grade, the volume and the destination port. You will have a quote, a specification sheet and samples within one business day."):
    return """<section class="cta-band">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <a href="%s" class="btn">Request a quote</a>
  </div>
</section>""" % (heading, text, rel(depth, "contact-us.html"))


def newsletter_band():
    return """<section class="cta-band">
  <div class="container">
    <h2>Not ready for a quote yet?</h2>
    <p>Subscribe to our weekly Vietnam spice market report for farm-gate and FOB prices, harvest conditions and freight rates.</p>
    <form class="newsletter-form" data-subject="Market report subscription" action="mailto:%s" method="post" enctype="text/plain">
      <input type="email" name="Email" placeholder="Your work email" required aria-label="Email address" />
      <button type="submit" class="btn">Subscribe</button>
      <div class="form-status" role="status"></div>
    </form>
  </div>
</section>""" % SALES_EMAIL


def documents_block():
    return """<div class="detail-block">
      <h3>Documents with every shipment</h3>
      <ul>
        <li>Phytosanitary certificate</li>
        <li>Certificate of origin</li>
        <li>Certificate of analysis</li>
        <li>Fumigation certificate</li>
        <li>Bill of lading, packing list, commercial invoice</li>
      </ul>
    </div>"""


def terms_block():
    return fmt("""<div class="detail-block">
      <h3>Order terms</h3>
      <ul>
        <li>Payment {payment}</li>
        <li>Packing to your specification</li>
        <li>Minimum order, lead time and Incoterms quoted per enquiry</li>
        <li>Private label available</li>
      </ul>
    </div>""")


def samples_block():
    return """<div class="detail-block">
      <h3>Samples</h3>
      <ul>
        <li>Pre-shipment samples before every first order</li>
        <li>Counter-samples retained against the shipped lot</li>
        <li>Courier to your QC lab on request</li>
      </ul>
    </div>"""


def forms_section(product):
    """Whole / cracked / ground, each with a description and its own photograph."""
    if not product.get("forms"):
        return ""
    blocks = []
    for title, body, best, img, alt in product["forms"]:
        text = """      <div>
        <h3>%s</h3>
        <p>%s</p>
        <p class="best-for">%s</p>
      </div>""" % (title, body, best)
        if img:
            blocks.append("""    <div class="form-row-block">
%s
      <figure>
        <img src="%s" alt="%s" loading="lazy" />
      </figure>
    </div>""" % (text, img, alt))
        else:
            # No photograph that accurately shows this cut — text runs full width
            # rather than borrowing a picture of something else.
            blocks.append("""    <div class="form-row-block no-photo">
%s
    </div>""" % text)
    rows = "\n".join(blocks)

    return """<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Forms</span>
      <h2>%s</h2>
      <p>%s</p>
    </div>
%s
  </div>
</section>

""" % (product["forms_heading"], product["forms_intro"], rows)


def related_block(depth, slugs):
    cards = "\n".join(
        '      <a href="%s"><strong>%s</strong><span>%s</span></a>'
        % (rel(depth, "products/%s.html" % s), PRODUCTS_BY_SLUG[s]["name"], PRODUCTS_BY_SLUG[s]["lede"])
        for s in slugs
    )
    return """<section class="features">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Also from Green Lotus</span>
      <h2>Related products</h2>
    </div>
    <div class="related">
%s
    </div>
  </div>
</section>""" % cards


# --------------------------------------------------------------------------
# Product pages
# --------------------------------------------------------------------------

def build_product(product):
    tables = "\n\n".join(spec_table(t) for t in product["tables"])
    origin = "\n      ".join("<p>%s</p>" % p for p in product["origin"])

    schema = """{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "%s",
  "description": "%s",
  "category": "Spices and food ingredients",
  "brand": { "@type": "Brand", "name": "Green Lotus Spices" },
  "countryOfOrigin": "VN",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "USD",
    "seller": { "@type": "Organization", "name": "Green Lotus Spice Company Limited" }
  }
}""" % (product["name"], product["description"])

    body = """<section class="product-hero">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../our-spices.html">Our Spices</a><span>/</span>%(name)s</div>
    <span class="eyebrow">Vietnamese origin</span>
    <h1>%(name)s</h1>
    <p style="max-width:680px">%(lede)s</p>
    <a href="#enquiry" class="btn" style="background:var(--green);color:#fff">Get a quote</a>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Specifications</span>
      <h2>%(name)s grades we ship</h2>
      <p>%(intro)s</p>
    </div>
%(tables)s
    <p class="table-note">Other grades and custom specifications are available on request. Certificates of analysis are issued per lot.</p>

    <div class="detail-grid">
%(documents)s
%(terms)s
%(samples)s
    </div>
  </div>
</section>

%(forms)s<section class="features">
  <div class="container split">
    <div>
      <span class="eyebrow">Sourcing</span>
      <h2>%(origin_heading)s</h2>
      %(origin)s
    </div>
    <img src="%(hero_img)s" alt="%(hero_alt)s" loading="lazy" />
  </div>
</section>

<section>
  <div class="container split">
    <div>
      <span class="eyebrow">Get a price</span>
      <h2>Request a quote for %(name)s</h2>
      <p>Send the grade and volume you need and we will price it, confirm lead time and send samples. If you are still choosing a grade, tell us the application and we will recommend one.</p>
      <p>Prefer email? Write to <a href="mailto:%(email)s">%(email)s</a>.</p>
    </div>
%(form)s
  </div>
</section>

%(related)s

%(cta)s""" % {
        "name": product["name"],
        "lede": product["lede"],
        "intro": product["intro"],
        "tables": tables,
        "forms": forms_section(product),
        "documents": documents_block(),
        "terms": terms_block(),
        "samples": samples_block(),
        "origin_heading": product["origin_heading"],
        "origin": origin,
        "hero_img": RANGE_IMG[product["slug"]][0],
        "hero_alt": RANGE_IMG[product["slug"]][1],
        "form": quote_form(1, "Quote request: %s" % product["name"], product["slug"]),
        "email": SALES_EMAIL,
        "related": related_block(1, product["related"]),
        "cta": cta_band(1),
    }

    return page(
        "products/%s.html" % product["slug"],
        product["title"],
        product["description"],
        body,
        depth=1,
        schema=schema,
        active="spices",
    )


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------

FEATURED = [c for c in RANGE_CARDS if c[0] in ("black-pepper", "cassia", "cashews")]


def build_index():
    cards = "\n".join("""      <div class="card">
        <img src="%s" alt="%s" loading="lazy" />
        <div class="card-body">
          <h3>%s</h3>
          <p>%s</p>
          <a class="card-link" href="products/%s.html">Specifications &rarr;</a>
        </div>
      </div>""" % (img, alt, PRODUCTS_BY_SLUG[slug]["name"], blurb, slug)
        for slug, img, alt, blurb in FEATURED)

    schema = """{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Green Lotus Spice Company Limited",
  "alternateName": ["Green Lotus Spices", "CÔNG TY TNHH GIA VỊ SEN XANH"],
  "url": "%s/",
  "email": "%s",
  "telephone": "+84889004111",
  "foundingDate": "2022",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Ho Chi Minh City",
    "addressCountry": "VN"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "sales",
    "email": "%s",
    "telephone": "+84889004111",
    "availableLanguage": ["English", "Vietnamese"]
  }
}""" % (DOMAIN, SALES_EMAIL, SALES_EMAIL)

    body = """<section class="hero">
  <div class="container">
    <span class="eyebrow" style="color:#bfe6c8">Vietnamese spice exporter</span>
    <h1>Vietnamese spices, shipped in container loads</h1>
    <p>Black and white pepper, cassia, star anise, cashews, dried chilli and desiccated coconut &mdash; sourced direct from growers and processed to your specification.</p>
    <a href="contact-us.html" class="btn">Request a quote</a>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-intro">
      <span class="eyebrow">What we ship</span>
      <h2>Spices</h2>
      <p>Cleaned, graded and sorted to export standard, with a certificate of analysis on every lot.</p>
    </div>

    <div class="grid">
%s
    </div>

    <div style="text-align:center;margin-top:52px">
      <a href="our-spices.html" class="btn" style="background:var(--green);color:#fff">See the full range</a>
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <div class="section-intro">
      <span class="eyebrow">Why buyers work with us</span>
      <h2>What you get from Green Lotus</h2>
    </div>
    <div class="feature-grid">
      <div class="feature">
        <h3>Direct from the farm gate</h3>
        <p>We buy through our own collection network in {provinces}, not through a chain of middlemen. That means traceable lots, a price that holds, and a straight answer when the crop moves.</p>
      </div>
      <div class="feature">
        <h3>Processed to your spec</h3>
        <p>Cleaning, grading, colour sorting, steam sterilisation and grinding, to ASTA, ESA or your own written specification. Samples before every first shipment.</p>
      </div>
      <div class="feature">
        <h3>Documented properly</h3>
        <p>A full export document set with every container &mdash; phytosanitary certificate, certificate of origin, certificate of analysis and fumigation certificate.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container split">
    <div>
      <span class="eyebrow">Who we supply</span>
      <h2>Large manufacturers and supermarkets</h2>
      <p>We supply large food manufacturers and supermarket groups in {markets}, alongside spice importers, contract grinders and private-label packers. Most start with a single container of one line and add products as the relationship settles.</p>
      <p>If you need a product we do not list, ask. We source to order across the Vietnamese spice trade and can quote on lines outside our seven.</p>
      <a href="about-us.html" class="btn" style="background:var(--green);color:#fff">About Green Lotus</a>
    </div>
    <img src="https://images.unsplash.com/photo-1678182451047-196f22a4143e?q=80&w=1400&auto=format&fit=crop" alt="Containers at a shipping terminal" loading="lazy" />
  </div>
</section>

<section class="newsletter">
  <div class="container">
    <h2>Vietnam spice prices, every week</h2>
    <p>Farm-gate and FOB movements on pepper, cassia and star anise, harvest conditions and freight rates. Written for buyers, free, and no sales calls.</p>
    <form class="newsletter-form" data-subject="Market report subscription" action="mailto:%s" method="post" enctype="text/plain">
      <input type="email" name="Email" placeholder="Your work email" required aria-label="Email address" />
      <button type="submit" class="btn">Send me the report</button>
      <div class="form-status" role="status"></div>
    </form>
  </div>
</section>""" % (cards, SALES_EMAIL)

    return page("index.html", "Vietnam Spice Exporter | Pepper, Cassia, Cashews | Green Lotus",
                "Vietnamese spice exporter supplying black and white pepper, cassia, star anise, cashews, dried chilli and desiccated coconut in bulk. Quotes within 24 hours.",
                body, depth=0, schema=schema, active="home")


# --------------------------------------------------------------------------
# Range
# --------------------------------------------------------------------------

def build_range():
    cards = "\n".join("""      <div class="card">
        <img src="%s" alt="%s" loading="lazy" />
        <div class="card-body">
          <h3>%s</h3>
          <p>%s</p>
          <a class="card-link" href="products/%s.html">Specifications &rarr;</a>
        </div>
      </div>""" % (img, alt, PRODUCTS_BY_SLUG[slug]["name"], blurb, slug)
        for slug, img, alt, blurb in RANGE_CARDS)

    body = """<section class="product-hero">
  <div class="container section-intro">
    <span class="eyebrow">Full range</span>
    <h1>Vietnamese spices and nuts in bulk</h1>
    <p>Seven export lines, each with published grades, moisture and density limits. Click any product for the full specification.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="grid">
%s
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Beyond the seven</span>
      <h2>Sourcing to order</h2>
      <p>We source additional lines across the Vietnamese spice and agricultural trade on request &mdash; turmeric, ginger, cardamom, coffee and others. If you have a requirement we do not list, send the specification and we will tell you honestly whether we can meet it.</p>
    </div>
  </div>
</section>

%s""" % (cards, cta_band(0))

    return page("our-spices.html", "Bulk Vietnamese Spices & Nuts | Product Range | Green Lotus",
                "Seven export-grade products from Vietnam with full specifications, grades and packaging detail. Request a quote on any line.",
                body, depth=0, active="spices")


# --------------------------------------------------------------------------
# About
# --------------------------------------------------------------------------

def build_about():
    body = """<section class="product-hero">
  <div class="container section-intro">
    <span class="eyebrow">The company</span>
    <h1>About Green Lotus Spices</h1>
    <p>Green Lotus Spice Company Limited is a Vietnamese spice exporter based in {city}. We have been exporting since {founded} and ship seven lines &mdash; pepper, cassia, star anise, cashews, dried chilli and desiccated coconut &mdash; to importers, grinders and food manufacturers in {markets}.</p>
  </div>
</section>

<section>
  <div class="container split">
    <div>
      <span class="eyebrow">At a glance</span>
      <h2>The company</h2>
      <table class="facts">
        <tr><th>Registered name</th><td>{company_name_full}</td></tr>
        <tr><th>Vietnamese name</th><td>{company_name_vn}</td></tr>
        <tr><th>Head office</th><td>{city}, Vietnam</td></tr>
        <tr><th>Exporting since</th><td>{founded}</td></tr>
        <tr><th>Export markets</th><td>{markets}</td></tr>
      </table>
    </div>
    <img src="https://images.unsplash.com/photo-1695098448374-e735208dad98?q=80&w=1400&auto=format&fit=crop" alt="Rice farmland in Vietnam" loading="lazy" />
  </div>
</section>

<section class="features">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">How we work</span>
      <h2>Direct buying, controlled processing</h2>
    </div>
    <div class="feature-grid">
      <div class="feature">
        <h3>How we buy</h3>
        <p>We buy through our own collection network in the growing regions rather than off the spot market &mdash; pepper from {provinces}, cassia from {cassia_provinces}, star anise from {anise_provinces}. Buying the same areas season after season is what lets us hold a specification.</p>
      </div>
      <div class="feature">
        <h3>How we control quality</h3>
        <p>Cleaning, grading, colour sorting and grinding run at facilities we know, under our own QC. Every lot is sampled before loading and a certificate of analysis travels with the shipment. A lot that misses specification does not ship.</p>
      </div>
      <div class="feature">
        <h3>What we commit to</h3>
        <p>Every shipment leaves with a phytosanitary certificate, certificate of origin, certificate of analysis and the full document set your customs broker needs. Additional certification to your market's requirements on request.</p>
      </div>
      <div class="feature">
        <h3>Where we source</h3>
        <p>Our own lines are Vietnamese. Where a customer needs an origin we do not grow, we say so plainly and source it as a trading line rather than presenting it as our own crop.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container split">
    <img src="https://images.unsplash.com/photo-1678182451047-196f22a4143e?q=80&w=1400&auto=format&fit=crop" alt="Containers at a shipping terminal" loading="lazy" />
    <div>
      <span class="eyebrow">Growers</span>
      <h2>The farmers we buy from</h2>
      <p>Sustainability language is cheap in this trade, so here is what ours amounts to: we buy from the same growing districts season after season, we pay at the farm gate where volume allows, and we keep the relationship rather than chasing whoever is cheapest in a given week.</p>
      <p>That continuity is what lets us hold a specification. A supplier buying spot cannot promise you the same lot profile twice.</p>
    </div>
  </div>
</section>

%s""" % cta_band(0)

    return page("about-us.html", "About Green Lotus Spice Company | Vietnamese Spice Exporter",
                "Vietnamese spice exporter based in Ho Chi Minh City, exporting since 2022 to Taiwan, Europe, the UAE and the USA. How we buy and how we control quality.",
                body, depth=0, active="about")


# --------------------------------------------------------------------------
# Quality and documents
# --------------------------------------------------------------------------
# Packaging and shipping
# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------

def build_contact():
    body = """<section class="product-hero">
  <div class="container section-intro">
    <span class="eyebrow">Get in touch</span>
    <h1>Contact Us</h1>
    <p>Enquire below for the products you require and we will get back to you within one business day.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="contact-grid">
      <div class="contact-block">
        <h3>Company</h3>
        <p>{company_name_full}</p>
        <p>{company_name_vn}</p>
        <p>{city}, Vietnam</p>
      </div>
      <div class="contact-block">
        <h3>Talk to us</h3>
        <p><a href="{phone_href}">{phone}</a></p>
        <p>Also on WhatsApp and Zalo</p>
        <p>Mon&ndash;Sat, 8am&ndash;6pm ICT (GMT+7)</p>
      </div>
      <div class="contact-block">
        <h3>Email</h3>
        <p>Sales and quotes<br><a href="mailto:%s">%s</a></p>
        <p>Documentation and accounts<br><a href="mailto:%s">%s</a></p>
      </div>
      <div class="contact-block">
        <h3>What happens next</h3>
        <p>We reply within one business day with a price, the specification sheet and samples if you want them.</p>
      </div>
    </div>
  </div>
</section>

<section class="features">
  <div class="container" style="max-width:820px">
%s
  </div>
</section>

%s""" % (SALES_EMAIL, SALES_EMAIL, ADMIN_EMAIL, ADMIN_EMAIL,
         quote_form(0, "Website enquiry"),
         newsletter_band())

    return page("contact-us.html", "Contact Green Lotus Spices | Request a Quote",
                "Send your specification and volume for a quote within one business day. Green Lotus Spice Company Limited, Ho Chi Minh City, Vietnam.",
                body, depth=0, active="contact")


# --------------------------------------------------------------------------
# sitemap / robots
# --------------------------------------------------------------------------

def build_sitemap(paths):
    urls = "\n".join(
        "  <url><loc>%s/%s</loc><changefreq>monthly</changefreq></url>" % (DOMAIN, p)
        for p in paths
    )
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
""" % urls
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as handle:
        handle.write(xml)

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as handle:
        handle.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)


def main():
    paths = [build_index(), build_range()]
    for product in PRODUCTS:
        paths.append(build_product(product))
    paths.append(build_about())
    paths.append(build_contact())
    build_sitemap(paths)

    remaining = 0
    leftover = set()
    for path in paths:
        with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
            text = handle.read()
        remaining += text.count('class="todo"')
        leftover |= set(re.findall(r"\{[a-z_]+\}", text))
    print("Built %d pages, sitemap.xml and robots.txt." % len(paths))
    print("%d placeholders still to fill." % remaining)
    if leftover:
        print("UNRESOLVED TOKENS: %s" % ", ".join(sorted(leftover)))


if __name__ == "__main__":
    main()
