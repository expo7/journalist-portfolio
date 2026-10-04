
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
  const artSelect = document.querySelector('#hero-art');
  if (artSelect) {
    function applyArt(value) {
      document.body.classList.remove('hero-art-lighthouse', 'hero-art-corkboard');
      document.body.classList.add('hero-art-' + value);
      artSelect.value = value;
    }
    try { const savedArt = sessionStorage.getItem('portfolio-preview-art'); if (['lighthouse', 'corkboard'].includes(savedArt)) applyArt(savedArt); } catch {}
    artSelect.addEventListener('change', () => { applyArt(artSelect.value); try { sessionStorage.setItem('portfolio-preview-art', artSelect.value); } catch {} });
  }
  select.addEventListener("change", () => {
    apply(select.value);
    try { sessionStorage.setItem("portfolio-preview-style", select.value); } catch {}
  });
})();
