document.addEventListener("DOMContentLoaded", () => {
  const THEME_KEY = "rmg_theme";
  const themeToggle = document.getElementById("theme-toggle");
  const backButton = document.getElementById("nav-back");

  function setTableHeaderTheme(theme) {
    const from = theme === "dark" ? "table-light" : "table-dark";
    const to = theme === "dark" ? "table-dark" : "table-light";
    document.querySelectorAll(`thead.${from}`).forEach((thead) => {
      thead.classList.remove(from);
      thead.classList.add(to);
    });
  }

  function getInitialTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function updateToggleText(theme) {
    if (!themeToggle) return;
    themeToggle.textContent = theme === "dark" ? "Light mode" : "Dark mode";
  }

  function applyTheme(theme) {
    const resolved = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-bs-theme", resolved);
    localStorage.setItem(THEME_KEY, resolved);
    updateToggleText(resolved);
    setTableHeaderTheme(resolved);
  }

  const initialTheme = getInitialTheme();
  applyTheme(initialTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current =
        document.documentElement.getAttribute("data-bs-theme") ||
        getInitialTheme();
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  if (backButton) {
    const fallbackUrl = backButton.dataset.fallback || "/";
    backButton.addEventListener("click", () => {
      window.location.assign(fallbackUrl);
    });
  }
});
