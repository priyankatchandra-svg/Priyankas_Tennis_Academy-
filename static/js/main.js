// ── Mobile nav ──────────────────────────────────────────────
const ham = document.getElementById('hamburger');
const nav = document.getElementById('nav-links');
if (ham && nav) ham.addEventListener('click', () => nav.classList.toggle('open'));

// ── Lesson type tiles ────────────────────────────────────────
document.querySelectorAll('.lt-tile').forEach(tile => {
  tile.addEventListener('click', () => {
    document.querySelectorAll('.lt-tile').forEach(t => t.classList.remove('selected'));
    tile.classList.add('selected');
  });
});

// ── Time slots ───────────────────────────────────────────────
document.querySelectorAll('.slot').forEach(slot => {
  slot.addEventListener('click', () => {
    document.querySelectorAll('.slot').forEach(s => s.classList.remove('selected'));
    slot.classList.add('selected');
  });
});

// ── Admin tabs ───────────────────────────────────────────────
const tabBtns   = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    tabPanels.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    const p = document.getElementById(btn.dataset.tab);
    if (p) p.classList.add('active');
  });
});
if (tabBtns.length) tabBtns[0].click();

// ── Score bars animate in ────────────────────────────────────
document.querySelectorAll('.score-fill').forEach(bar => {
  const w = bar.style.width; bar.style.width = '0';
  setTimeout(() => { bar.style.width = w; }, 300);
});

// ── Flash auto-dismiss ───────────────────────────────────────
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .5s'; el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  }, 5000);
});
