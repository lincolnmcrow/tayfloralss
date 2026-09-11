import re
from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# Keep Tay's Instagram profile information visible.
if "@tayfloralss_" not in html:
    instagram = '''
<section class="sec blush" id="instagram">
  <div class="w">
    <div class="head">
      <div class="ey">Follow my creations</div>
      <h2>Tay Florals on Instagram.</h2>
      <p>See recent creations, floral ideas, and behind-the-scenes work from Tay.</p>
    </div>
    <div style="background:#fff;border:1px solid #ecd8dd;border-radius:24px;padding:28px;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:16px">
        <div style="width:64px;height:64px;border-radius:50%;overflow:hidden;background:#f7dbe4;flex:none">
          <img src="images/ig/pfp-new.jpg" alt="Tay Florals" style="width:100%;height:100%;object-fit:cover">
        </div>
        <div>
          <strong style="display:block;font:700 1.35rem Fraunces,serif">Naba Tay | DFW Florist</strong>
          <span style="color:#b3123a;font-weight:700">@tayfloralss_</span>
          <div style="font-size:.86rem;color:#73585d;margin-top:3px">Dallas–Fort Worth · 3-day notice required</div>
          <div style="font-size:.82rem;color:#73585d">1,138 followers · 589 following</div>
        </div>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn" href="https://www.instagram.com/tayfloralss_/" target="_blank" rel="noopener">Follow on Instagram</a>
        <a class="btn light" href="#order">Request Something Similar</a>
      </div>
    </div>
  </div>
</section>
'''
    pattern = r'(<section class="hero".*?</section>)\s*(<section)'
    html, count = re.subn(pattern, r'\1\n' + instagram + r'\n\2', html, count=1, flags=re.S)
    if count != 1:
        html = html.replace('</main>', instagram + '\n</main>', 1)

# Remove the Fall video section (Google Drive embed) if an earlier build added it.
fall_video_pattern = r'\s*<section class="sec seasonal" id="fall-video">.*?</section>'
html = re.sub(fall_video_pattern, '', html, count=1, flags=re.S)

# Enforce Tay's 3-day notice rule in the inquiry date picker.
if 'TAY_DATE_RULE' not in html:
    date_js = '''
<script id="TAY_DATE_RULE">
(() => {
  const setup = () => {
    const dateInput = document.querySelector('input[type="date"]');
    if (!dateInput) return;
    const min = new Date();
    min.setHours(0,0,0,0);
    min.setDate(min.getDate() + 3);
    const yyyy = min.getFullYear();
    const mm = String(min.getMonth()+1).padStart(2,'0');
    const dd = String(min.getDate()).padStart(2,'0');
    dateInput.min = `${yyyy}-${mm}-${dd}`;
    dateInput.addEventListener('input', () => {
      if (dateInput.value && dateInput.value < dateInput.min) dateInput.value = '';
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
  else setup();
})();
</script>
'''
    html = html.replace('</body>', date_js + '\n</body>', 1)

# Favicon + stronger social preview metadata.
if 'href="/favicon.svg"' not in html:
    html = html.replace('</head>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n</head>', 1)
if 'og:image' not in html:
    tags = '''
<meta property="og:url" content="https://tayfloralss.netlify.app/">
<meta property="og:image" content="https://tayfloralss.netlify.app/images/gallery/bouquet-all-34.jpg">
<meta property="og:image:alt" content="Tay Florals custom bouquet">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Tay Florals | Custom Florals in DFW">
<meta name="twitter:description" content="Custom bouquets and floral gifts across the DFW area.">
<meta name="twitter:image" content="https://tayfloralss.netlify.app/images/gallery/bouquet-all-34.jpg">
'''
    html = html.replace('</head>', tags + '</head>', 1)

path.write_text(html, encoding='utf-8')
print('Tay Florals final production patch applied')
