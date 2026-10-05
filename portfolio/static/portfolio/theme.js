
(() => {
  const select = document.querySelector("#page-style");
  const harbor = document.querySelector("#harbor-theme");
  const rose = document.querySelector("#rose-theme");
  const midnight = document.querySelector("#midnight-theme");
  const glow = document.querySelector("#glow-theme");
  const themes = ["original", "harbor", "rose", "midnight", "glow"];
  if (!select || !harbor || !rose || !midnight || !glow) return;
  function apply(theme) {
    harbor.disabled = theme === "original";
    rose.disabled = theme !== "rose";
    midnight.disabled = !["midnight", "glow"].includes(theme);
    glow.disabled = theme !== "glow";
    document.body.classList.remove(...themes.map(item => "theme-" + item));
    document.body.classList.add("theme-" + theme);
    select.value = theme;
  }
  try {
    const saved = sessionStorage.getItem("portfolio-preview-style");
    if (themes.includes(saved)) apply(saved);
  } catch {}
  const navSelect = document.querySelector('#page-nav');
  if (navSelect) {
    function applyNav(value) { document.body.dataset.nav = value; navSelect.value = value; }
    try { const saved = sessionStorage.getItem('portfolio-preview-nav'); if (['scrolling', 'pinned'].includes(saved)) applyNav(saved); } catch {}
    navSelect.addEventListener('change', () => { applyNav(navSelect.value); try { sessionStorage.setItem('portfolio-preview-nav', navSelect.value); } catch {} });
  }
  const logoSelect = document.querySelector('#page-logo');
  if (logoSelect) {
    const available = [...logoSelect.options].map(option => option.value);
    function applyLogo(value) { document.body.dataset.logo = value; logoSelect.value = value; }
    try { const saved = sessionStorage.getItem('portfolio-preview-logo'); if (available.includes(saved)) applyLogo(saved); } catch {}
    logoSelect.addEventListener('change', () => { applyLogo(logoSelect.value); try { sessionStorage.setItem('portfolio-preview-logo', logoSelect.value); } catch {} });
  }
  const artSelect = document.querySelector('#hero-art');
  if (artSelect) {
    const frames = ['.harbor-visual', '.corkboard-visual', '.portrait-visual', '.observer-visual', '.poolcat-visual'].map(selector => document.querySelector(selector));
    const pause = document.querySelector('#hero-pause');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    let timer, index = 0, paused = reduced.matches;
    function stop() { clearInterval(timer); }
    function advance() {
      frames[index].classList.remove('hero-frame-active');
      frames[index].setAttribute('aria-hidden', 'true');
      index = (index + 1) % frames.length;
      frames[index].classList.add('hero-frame-active');
      frames[index].setAttribute('aria-hidden', 'false');
    }
    function start() {
      stop();
      if (artSelect.value === 'rotate' && !paused && !document.hidden) timer = setInterval(advance, 6000);
    }
    function applyArt(value) {
      stop();
      document.body.classList.remove('hero-art-lighthouse', 'hero-art-corkboard', 'hero-art-portrait', 'hero-art-observer', 'hero-art-rotate', 'hero-art-poolcat');
      document.body.classList.add('hero-art-' + value);
      artSelect.value = value;
      pause.hidden = value !== 'rotate';
      frames.forEach((frame, i) => { frame.classList.toggle('hero-frame-active', i === index); frame.setAttribute('aria-hidden', value === 'rotate' && i !== index ? 'true' : 'false'); });
      pause.textContent = paused ? 'Play images' : 'Pause images';
      start();
    }
    pause.addEventListener('click', () => { paused = !paused; pause.textContent = paused ? 'Play images' : 'Pause images'; start(); });
    document.addEventListener('visibilitychange', start);
    reduced.addEventListener('change', () => { if (reduced.matches) { paused = true; pause.textContent = 'Play images'; stop(); } });
    try { const savedArt = sessionStorage.getItem('portfolio-preview-art'); if (['lighthouse', 'corkboard', 'portrait', 'observer', 'poolcat', 'rotate'].includes(savedArt)) applyArt(savedArt); } catch {}
    artSelect.addEventListener('change', () => { applyArt(artSelect.value); try { sessionStorage.setItem('portfolio-preview-art', artSelect.value); } catch {} });
  }
  select.addEventListener("change", () => {
    apply(select.value);
    try { sessionStorage.setItem("portfolio-preview-style", select.value); } catch {}
  });
})();
