# Before this goes live

No placeholders remain on any page. Two things still need a decision.

## 1. Check the specification figures

The tables in `tools/products.py` are standard Vietnamese export grades taken
from common trade practice — **not Green Lotus lab data**. A published
specification is a commitment to the buyer, so check each figure against your
own certificates of analysis. A buyer who receives 12.8% moisture against a
12.5% claim on your website has a claim against you.

Also confirm the growing regions written into the sourcing copy match where you
actually buy:

| Product | Regions stated |
| --- | --- |
| Black and white pepper | Dak Lak, Gia Lai, Dong Nai, Binh Phuoc |
| Cassia | Yen Bai, Quang Nam, Thanh Hoa |
| Star anise | Lang Son, Cao Bang |
| Cashews | Binh Phuoc, Dong Nai |
| Dried chilli | Mekong Delta, central coast |
| Desiccated coconut | Ben Tre, Tra Vinh |

## 2. Wire up the enquiry forms

The forms currently fall back to opening the visitor's mail client, which is
what the old site did and why enquiries were being lost. Create a free endpoint
at [Formspree](https://formspree.io) or [Web3Forms](https://web3forms.com) and
paste the URL into `window.GL_FORM_ENDPOINT` at the top of `assets/site.js`.

## Held back deliberately

These are not on the site because you asked to leave them off. Each is defined
in the `F` dictionary in `tools/build.py` — add a value there and rebuild when
you want it published.

- Business registration number and tax code
- Office and warehouse addresses
- Annual volume, containers per year, headcount, warehouse capacity
- Minimum order quantity, lead time, port of loading, Incoterms
- Packing weights and container quantities
- Certifications, and the name of your testing laboratory
- Named contacts for sales, documentation and management

The two that cost you most enquiries are the **address** and the
**certifications** — they are the first things an importer's procurement team
looks for before they will open an account.

## Also worth doing

- Redirect `greenlotusvn.com` to `www.greenlotusvn.com` (or the reverse) in
  Vercel, so Google stops splitting the ranking between two copies of the site.
- Replace the stock farm photography with your own warehouse, processing line
  and loading photos.
- Publish the weekly market report — it is the strongest SEO asset you have and
  it is currently invisible to Google.
