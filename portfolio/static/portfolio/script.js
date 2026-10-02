const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const filters = document.querySelectorAll(".filter");
const stories = document.querySelectorAll(".story-card");
const filterMessage = document.querySelector("#filter-message");
const copyEmail = document.querySelector("#copy-email");

navToggle.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("is-open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
  nav.classList.remove("is-open");
  navToggle.setAttribute("aria-expanded", "false");
}));

filters.forEach((filter) => filter.addEventListener("click", () => {
  const category = filter.dataset.filter;
  filters.forEach((item) => item.classList.toggle("is-active", item === filter));
  let visible = 0;

  stories.forEach((story) => {
    const shouldShow = category === "all" || story.dataset.category === category;
    story.classList.toggle("is-hidden", !shouldShow);
    if (shouldShow) visible += 1;
  });

  filterMessage.textContent = category === "all" ? `Showing all ${visible} stories.` : `Showing ${visible} ${category}.`;
}));

copyEmail.addEventListener("click", async () => {
  const email = copyEmail.dataset.email;
  try {
    await navigator.clipboard.writeText(email);
    copyEmail.textContent = "Email copied";
  } catch {
    copyEmail.textContent = email;
  }
});

document.querySelector("#year").textContent = new Date().getFullYear();
