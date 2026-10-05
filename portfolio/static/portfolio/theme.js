
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
    function applyArt(value) {
      document.body.classList.remove('hero-art-lighthouse', 'hero-art-corkboard', 'hero-art-portrait', 'hero-art-observer');
      document.body.classList.add('hero-art-' + value);
      artSelect.value = value;
    }
    try { const savedArt = sessionStorage.getItem('portfolio-preview-art'); if (['lighthouse', 'corkboard', 'portrait', 'observer'].includes(savedArt)) applyArt(savedArt); } catch {}
    artSelect.addEventListener('change', () => { applyArt(artSelect.value); try { sessionStorage.setItem('portfolio-preview-art', artSelect.value); } catch {} });
  }
  select.addEventListener("change", () => {
    apply(select.value);
    try { sessionStorage.setItem("portfolio-preview-style", select.value); } catch {}
  });
})();
