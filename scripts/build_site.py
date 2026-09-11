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
'''

# Always inject the latest hero fix on each Netlify build.
# This is intentionally unconditional so later CSS changes are applied even if an older
# HERO READABILITY FIX block already exists in index.html.
marker = "/* HERO READABILITY FIX */"
if marker in html:
    start = html.index(marker)
    end = html.find("/* SEASONAL SPOTLIGHT */", start)
    if end != -1:
        html = html[:start] + css.strip() + "\n" + html[end:]
    else:
        html = html.replace("</style>", css + "\n</style>", 1)
else:
    html = html.replace("</style>", css + "\n</style>", 1)

seasonal = r'''
<section class="sec seasonal" id="seasonal">
  <div class="w seasonalGrid">
    <div class="seasonalArt">
      <img src="images/gallery/bouquet-all-34.jpg" alt="Tay Florals seasonal bouquet">
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

path.write_text(html, encoding="utf-8")
print("Tay Florals build enhancements applied")
