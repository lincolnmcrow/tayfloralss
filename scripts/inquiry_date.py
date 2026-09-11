from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

marker = "/* TAY 3-DAY INQUIRY RULE */"
if marker not in html:
    script = r'''<script>
/* TAY 3-DAY INQUIRY RULE */
(() => {
  const dateInput = document.querySelector('#date');
  if (!dateInput) return;

  const minimum = new Date();
  minimum.setHours(0, 0, 0, 0);
  minimum.setDate(minimum.getDate() + 3);

  const yyyy = minimum.getFullYear();
  const mm = String(minimum.getMonth() + 1).padStart(2, '0');
  const dd = String(minimum.getDate()).padStart(2, '0');
  const minDate = `${yyyy}-${mm}-${dd}`;

  dateInput.min = minDate;
  dateInput.setAttribute('min', minDate);
  dateInput.title = 'Tay Floralss requires at least 3 days notice.';

  dateInput.addEventListener('input', () => {
    if (dateInput.value && dateInput.value < minDate) {
      dateInput.value = '';
      dateInput.setCustomValidity('Please choose a date at least 3 days from today.');
    } else {
      dateInput.setCustomValidity('');
    }
  });

  dateInput.addEventListener('change', () => {
    if (dateInput.value && dateInput.value < minDate) {
      dateInput.value = '';
      dateInput.setCustomValidity('Please choose a date at least 3 days from today.');
    } else {
      dateInput.setCustomValidity('');
    }
  });
})();
</script>
'''
    html = html.replace('</body>', script + '</body>', 1)
    path.write_text(html, encoding='utf-8')
    print('3-day inquiry date rule applied')
else:
    print('3-day inquiry date rule already present')
