
(() => {
  const select = document.querySelector("#page-style");
  const harbor = document.querySelector("#harbor-theme");
  const rose = document.querySelector("#rose-theme");
  const midnight = document.querySelector("#midnight-theme");
  const themes = ["original", "harbor", "rose", "midnight"];
  if (!select || !harbor || !rose || !midnight) return;
  function apply(theme) {
    harbor.disabled = theme === "original";
    rose.disabled = theme !== "rose";
    midnight.disabled = theme !== "midnight";
    document.body.classList.remove(...themes.map(item => "theme-" + item));
    document.body.classList.add("theme-" + theme);
    select.value = theme;
  }
  try {
    const saved = sessionStorage.getItem("portfolio-preview-style");
    if (themes.includes(saved)) apply(saved);
  } catch {}
  select.addEventListener("change", () => {
    apply(select.value);
    try { sessionStorage.setItem("portfolio-preview-style", select.value); } catch {}
  });
})();
