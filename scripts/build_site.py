from pathlib import Path
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")

css = r'''
/* HERO READABILITY FIX */
.hero:after{background:linear-gradient(90deg,rgba(8,2,5,.78) 0%,rgba(8,2,5,.60) 34%,rgba(8,2,5,.30) 62%,rgba(8,2,5,.42) 100%),linear-gradient(180deg,rgba(8,2,5,.18) 0%,rgba(8,2,5,.35) 45%,rgba(8,2,5,.88) 100%)!important}
.heroCopy{max-width:820px;padding:100px 0 76px;text-shadow:0 3px 22px rgba(0,0,0,.72)}
.heroCopy:before{content:"";position:absolute;z-index:-1;left:-45px;top:55px;bottom:35px;width:min(780px,88vw);background:linear-gradient(90deg,rgba(12,2,7,.52),rgba(12,2,7,.22),transparent);filter:blur(18px);pointer-events:none}
.hero h1{color:#fff!important;text-shadow:0 4px 30px rgba(0,0,0,.85),0 1px 2px rgba(0,0,0,.95)}
.hero p{color:#fff!important;text-shadow:0 3px 14px rgba(0,0,0,.82);font-weight:500}
.hero .kicker{color:#fff!important;text-shadow:0 3px 12px rgba(0,0,0,.8);font-weight:700}
.heroNote{color:#fff!important;text-shadow:0 3px 12px rgba(0,0,0,.8)}
.heroBtns .btn{box-shadow:0 7px 25px rgba(0,0,0,.32)}
.heroBtns .btn.light{background:#fff!important;color:#b3123a!important;border-color:#fff!important}
@media(max-width:650px){.heroCopy{padding:72px 0 48px}.heroCopy:before{left:-25px;top:30px;bottom:20px;width:105vw;background:rgba(12,2,7,.38);filter:blur(20px)}.hero:after{background:linear-gradient(180deg,rgba(8,2,5,.30),rgba(8,2,5,.52) 42%,rgba(8,2,5,.93) 100%)!important}}

/* SEASONAL SPOTLIGHT */
.seasonal{position:relative;overflow:hidden;background:#f7eee9;color:#241214}
.seasonal:before{content:"";position:absolute;width:420px;height:420px;border-radius:50%;background:rgba(179,18,58,.07);right:-140px;top:-180px}
.seasonalGrid{display:grid;grid-template-columns:1.05fr .95fr;gap:55px;align-items:center}
.seasonalArt{position:relative;border-radius:28px;overflow:hidden;box-shadow:0 20px 60px rgba(86,17,35,.16);transform:rotate(-1deg)}
.seasonalArt img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}
.seasonalBadge{position:absolute;left:18px;bottom:18px;background:#fff;border:1px solid #ecd8dd;border-radius:999px;padding:9px 13px;font:700 .68rem "Space Mono",monospace;color:#b3123a;text-transform:uppercase;letter-spacing:.08em}
.seasonalCopy{position:relative;z-index:1}
.seasonalCopy h2{font:700 clamp(2.6rem,5vw,4.8rem)/.98 Fraunces,serif;letter-spacing:-.04em;margin:12px 0 18px}
.seasonalCopy p{max-width:58ch;color:#73585d;font-size:1.05rem}
.seasonalBullets{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:25px 0}
.seasonalBullets div{background:rgba(255,255,255,.72);border:1px solid #ecd8dd;border-radius:14px;padding:14px;font-weight:600}
.seasonalBullets span{display:block;color:#73585d;font-size:.82rem;font-weight:400;margin-top:2px}
@media(max-width:980px){.seasonalGrid{grid-template-columns:1fr;gap:35px}.seasonalArt{order:2}}
@media(max-width:650px){.seasonalBullets{grid-template-columns:1fr}.seasonalArt img{aspect-ratio:1/1}}

/* PRODUCTION POLISH */
html{scroll-padding-top:90px}
img{content-visibility:auto}
.gallery img,.serviceImg img,.occasion img{will-change:transform}
.mobileNavOpen{overflow:hidden}
@media(max-width:980px){
  .navin{position:relative}
  .links.mobileOpen{display:flex;position:absolute;left:0;right:0;top:74px;background:rgba(255,255,255,.98);backdrop-filter:blur(18px);border:1px solid var(--l);border-top:0;border-radius:0 0 18px 18px;padding:16px;flex-direction:column;align-items:stretch;gap:4px;box-shadow:0 18px 35px rgba(36,18,20,.12)}
  .links.mobileOpen a{padding:12px;border-radius:10px}
  .links.mobileOpen a:hover{background:var(--b)}
}
.mobileMenuButton{display:none}
.formSuccess{display:none;margin:0 0 18px;padding:15px 16px;border-radius:14px;background:#edf5ea;border:1px solid #cfe2c8;color:#31522b;font-weight:600}
.formSuccess.show{display:block}
.serviceArea{background:#fff;border-top:1px solid var(--l);border-bottom:1px solid var(--l)}
.serviceAreaGrid{display:grid;grid-template-columns:1fr auto;gap:35px;align-items:center}
.serviceArea h2{font:700 clamp(2.2rem,4vw,3.8rem)/1 Fraunces,serif;margin:10px 0}
.serviceArea p{max-width:65ch;color:var(--m);margin:0}
.serviceAreaBadge{display:flex;align-items:center;gap:10px;padding:13px 16px;border:1px solid var(--l);border-radius:999px;background:var(--b);font:700 .7rem "Space Mono",monospace;color:var(--r);text-transform:uppercase;white-space:nowrap}
@media(max-width:650px){.serviceAreaGrid{grid-template-columns:1fr}.serviceAreaBadge{justify-self:start}.serviceArea{padding:60px 0!important}}
'''

marker = "/* HERO READABILITY FIX */"
if marker in html:
    start = html.index(marker)
    end = html.find("/* SEASONAL SPOTLIGHT */", start)
    if end != -1:
        seasonal_marker_end = html.find("</style>", end)
        if seasonal_marker_end != -1:
            html = html[:start] + css.strip() + "\n" + html[seasonal_marker_end:]
        else:
            html = html[:start] + css.strip() + "\n" + html[end:]
    else:
        html = html.replace("</style>", css + "\n</style>", 1)
else:
    html = html.replace("</style>", css + "\n</style>", 1)

seasonal = r'''
<section class="sec seasonal" id="seasonal">
  <div class="w seasonalGrid">
    <div class="seasonalArt">
      <img src="images/gallery/bouquet-all-34.jpg" alt="Tay Floralss seasonal bouquet">
      <div class="seasonalBadge">Seasonal spotlight · Fall</div>
    </div>
    <div class="seasonalCopy">
      <div class="ey">Seasonal spotlight</div>
      <h2>Fall flowers are here.</h2>
      <p>Bring the season into your next bouquet with warm, romantic tones and a custom design made around your occasion. Tell Tay what you are celebrating and ask about current seasonal colors, flowers, and availability.</p>
      <div class="seasonalBullets">
        <div>Warm seasonal colors<span>Think burgundy, blush, cream, and autumn tones.</span></div>
        <div>Made to order<span>Your arrangement can be shaped around your person and occasion.</span></div>
        <div>Fresh or eternal<span>Choose the style that fits your moment.</span></div>
        <div>DFW area<span>Ask about local delivery and availability.</span></div>
      </div>
      <a class="btn" href="#order">Ask about Fall Flowers</a>
    </div>
  </div>
</section>
'''

if 'id="seasonal"' not in html:
    pattern = r'(<section class="hero".*?</section>)\s*(<section)'
    html, count = re.subn(pattern, r'\1\n' + seasonal + r'\n\2', html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("Could not locate hero section insertion point")

# Production SEO metadata
head_end = html.find("</head>")
if head_end != -1:
    seo_tags = '''
<link rel="canonical" href="https://tayfloralss.netlify.app/">
<meta property="og:url" content="https://tayfloralss.netlify.app/">
<meta property="og:image" content="https://tayfloralss.netlify.app/images/gallery/bouquet-all-01.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Tay Floralss | Custom Florals in DFW">
<meta name="twitter:description" content="Custom bouquets, floral gifts, fresh flowers, eternal arrangements, and local DFW delivery.">
<meta name="twitter:image" content="https://tayfloralss.netlify.app/images/gallery/bouquet-all-01.jpg">
'''
    if 'rel="canonical"' not in html:
        html = html[:head_end] + seo_tags + html[head_end:]

# Add structured data for local discovery without inventing a street address.
if 'application/ld+json' not in html:
    schema = r'''
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Florist",
  "name":"Tay Floralss",
  "url":"https://tayfloralss.netlify.app/",
  "description":"Custom bouquets and floral gifts serving the Dallas–Fort Worth area.",
  "areaServed":"Dallas–Fort Worth, Texas",
  "sameAs":["https://www.instagram.com/tayfloralss_/"],
  "image":"https://tayfloralss.netlify.app/images/gallery/bouquet-all-01.jpg"
}
</script>
'''
    html = html.replace('</head>', schema + '</head>', 1)

# Add a focused DFW service-area reassurance section before the ordering section.
if 'id="service-area"' not in html:
    area = r'''
<section class="sec serviceArea" id="service-area">
  <div class="w serviceAreaGrid">
    <div>
      <div class="ey">Local florist</div>
      <h2>Made for the DFW area.</h2>
      <p>Tay Floralss creates custom arrangements for moments big and small across the Dallas–Fort Worth area. For local orders, ask about current delivery availability. Eternal arrangements may also be available for shipping outside the local area.</p>
    </div>
    <div class="serviceAreaBadge">♡ DFW floral delivery</div>
  </div>
</section>
'''
    html = re.sub(r'(<section[^>]+id="order"[^>]*>)', area + r'\n\1', html, count=1)

# Improve image loading and accessibility on the generated page.
html = re.sub(r'<img(?![^>]*\bloading=)', '<img loading="lazy" decoding="async"', html)
html = html.replace('class="media"', 'class="media" aria-hidden="true"')

# Keep hero videos from being downloaded unnecessarily on reduced-motion devices.
if 'data-hero-video' not in html:
    html = html.replace('<video ', '<video data-hero-video ', 3)

# Mobile navigation, inquiry confirmation, lightbox keyboard controls and form polish.
if '/* TAY PRODUCTION JS */' not in html:
    js = r'''
<script>
/* TAY PRODUCTION JS */
(() => {
  const menu = document.querySelector('.menu');
  const links = document.querySelector('.links');
  if (menu && links) {
    menu.setAttribute('aria-expanded','false');
    menu.setAttribute('aria-label','Open navigation');
    menu.addEventListener('click', () => {
      const open = links.classList.toggle('mobileOpen');
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      document.body.classList.toggle('mobileNavOpen', open);
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('mobileOpen');
      menu.setAttribute('aria-expanded','false');
      menu.setAttribute('aria-label','Open navigation');
      document.body.classList.remove('mobileNavOpen');
    }));
  }

  const form = document.querySelector('form[name="order"]');
  if (form) {
    form.setAttribute('action','/?success=1#order');
    const phone = Array.from(form.querySelectorAll('input')).find(i => /phone/i.test(i.name || i.id || ''));
    if (phone) phone.required = false;
    if (new URLSearchParams(location.search).get('success') === '1') {
      let note = document.querySelector('.formSuccess');
      if (!note) {
        note = document.createElement('div');
        note.className = 'formSuccess show';
        note.textContent = 'Your request is on its way 💌 Tay will review your idea and get back to you soon.';
        form.prepend(note);
      }
    }
  }

  const modal = document.querySelector('.modal');
  const modalImg = modal && modal.querySelector('img');
  const galleryButtons = Array.from(document.querySelectorAll('.gallery button'));
  let galleryIndex = 0;
  function showGallery(i) {
    if (!modal || !modalImg || !galleryButtons.length) return;
    galleryIndex = (i + galleryButtons.length) % galleryButtons.length;
    const image = galleryButtons[galleryIndex].querySelector('img');
    if (!image) return;
    modalImg.src = image.src;
    modalImg.alt = image.alt || 'Tay Floralss bouquet';
  }
  galleryButtons.forEach((button,i) => button.addEventListener('click', () => {
    galleryIndex = i;
    const image = button.querySelector('img');
    if (image && modalImg) modalImg.src = image.src;
  }));
  document.addEventListener('keydown', e => {
    if (!modal || !modal.classList.contains('open')) return;
    if (e.key === 'Escape') modal.classList.remove('open');
    if (e.key === 'ArrowRight') showGallery(galleryIndex + 1);
    if (e.key === 'ArrowLeft') showGallery(galleryIndex - 1);
  });

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) document.querySelectorAll('[data-hero-video]').forEach(v => v.removeAttribute('autoplay'));
})();
</script>
'''
    html = html.replace('</body>', js + '\n</body>', 1)

# Make the first above-the-fold gallery/service images available immediately; defer the rest.
first_images = 0
def eager_first(match):
    global first_images
    first_images += 1
    tag = match.group(0)
    if first_images <= 3:
        tag = tag.replace('loading="lazy"','loading="eager"',1)
    return tag
html = re.sub(r'<img[^>]*loading="lazy"[^>]*>', eager_first, html)

path.write_text(html, encoding="utf-8")
print("Tay Floralss production polish applied")
