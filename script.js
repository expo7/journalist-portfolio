const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const filters = document.querySelectorAll(".filter");
const stories = document.querySelectorAll(".story-card");
const filterMessage = document.querySelector("#filter-message");
const newsletterForm = document.querySelector("#newsletter-form");
const formMessage = document.querySelector("#form-message");
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

  filterMessage.textContent = category === "all" ? "Showing all 3 stories." : `Showing ${visible} ${category}.`;
}));

newsletterForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const email = new FormData(newsletterForm).get("email");
  formMessage.textContent = `Thanks — the next dispatch will go to ${email}.`;
  newsletterForm.reset();
});

copyEmail.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText("hello@candishart.com");
    copyEmail.textContent = "Email copied";
  } catch {
    copyEmail.textContent = "hello@candishart.com";
  }
});

document.querySelector("#year").textContent = new Date().getFullYear();
