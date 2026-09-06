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
    const el = document.querySelector('.category-nav');
    if (!el) return;
    el.classList.toggle('fade-left', nav.scrollLeft > 4);
    el.classList.toggle('fade-right', nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 4);
  }
  if (nav) {
    updateFade();
    nav.addEventListener('scroll', updateFade, { passive: true });
    window.addEventListener('resize', updateFade);
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
