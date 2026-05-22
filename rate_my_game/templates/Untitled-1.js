<!-- filepath: /home/shubh/Documents/BCIT Term 2.5/Agile-Development-Project/rate_my_game/static/js/ui.js -->
document.addEventListener("DOMContentLoaded", () => {
  const THEME_KEY = "rmg_theme";
  const themeToggle = document.getElementById("theme-toggle");

  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === "light" || stored === "dark") {
      return stored;
    }

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
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-bs-theme") || getPreferredTheme();
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  applyTheme(getPreferredTheme());
});