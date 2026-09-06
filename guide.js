(function () {
  const links = [...document.querySelectorAll('.nav-inner a')];
  const sections = [...document.querySelectorAll('main .category')];
  const catIds = sections.map((s) => s.id);
  if (!sections.length) return;

  function activate(id, { moveNav = true } = {}) {
    if (!catIds.includes(id)) id = catIds[0];
    sections.forEach((s) => {
      s.hidden = s.id !== id;
    });
    links.forEach((l) => l.setAttribute('aria-current', String(l.hash === '#' + id)));
    if (history.replaceState) history.replaceState(null, '', '#' + id);
    if (moveNav) {
      const activeLink = links.find((l) => l.hash === '#' + id);
      if (activeLink) activeLink.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    }
  }

  links.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      activate(link.hash.slice(1));
      document.getElementById('guia').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  const initial = location.hash && catIds.includes(location.hash.slice(1)) ? location.hash.slice(1) : catIds[0];
  activate(initial, { moveNav: false });

  const nav = document.querySelector('.nav-inner');
  function updateFade() {
    if (!nav) return;
    nav.classList.toggle('fade-left', nav.scrollLeft > 4);
    nav.classList.toggle('fade-right', nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 4);
  }
  if (nav) {
    updateFade();
    nav.addEventListener('scroll', updateFade, { passive: true });
    window.addEventListener('resize', updateFade);
  }

  const surpriseBtn = document.getElementById('surprise-btn');
  const surpriseView = document.getElementById('surprise-view');
  const surpriseCard = document.getElementById('surprise-card');
  const surpriseBack = document.getElementById('surprise-back');
  const categoryNav = document.querySelector('.category-nav');
  const introEl = document.querySelector('.intro');
  const mainEl = document.getElementById('guia');

  if (surpriseBtn && surpriseView && surpriseCard && surpriseBack && mainEl) {
    surpriseBtn.addEventListener('click', () => {
      const cards = [...document.querySelectorAll('main .card')];
      if (!cards.length) return;
      const pick = cards[Math.floor(Math.random() * cards.length)].cloneNode(true);
      pick.querySelectorAll('img').forEach((img) => (img.loading = 'eager'));
      surpriseCard.replaceChildren(pick);
      introEl.hidden = true;
      categoryNav.hidden = true;
      mainEl.hidden = true;
      surpriseView.hidden = false;
      window.scrollTo({ top: 0, behavior: 'instant' });
    });
    surpriseBack.addEventListener('click', () => {
      surpriseView.hidden = true;
      introEl.hidden = false;
      categoryNav.hidden = false;
      mainEl.hidden = false;
      window.scrollTo({ top: 0, behavior: 'instant' });
    });
  }

  const topBtn = document.createElement('button');
  topBtn.type = 'button';
  topBtn.className = 'float-top';
  topBtn.setAttribute('aria-label', 'Volver arriba');
  topBtn.textContent = '↑';
  topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  document.body.appendChild(topBtn);
  window.addEventListener(
    'scroll',
    () => topBtn.classList.toggle('show', window.scrollY > 700),
    { passive: true }
  );
})();
