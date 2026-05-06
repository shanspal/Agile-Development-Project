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

  function applyTheme(theme) {
    const resolved = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-bs-theme", resolved);
    localStorage.setItem(THEME_KEY, resolved);
    if (themeToggle) themeToggle.checked = resolved === "dark";
    setTableHeaderTheme(resolved);
  }

  function getInitialTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia?.("(prefers-color-scheme: dark)")?.matches
      ? "dark"
      : "light";
  }

  applyTheme(getInitialTheme());

  if (themeToggle) {
    themeToggle.addEventListener("change", () => {
      applyTheme(themeToggle.checked ? "dark" : "light");
    });
  }

  if (backButton) {
    const fallbackUrl = backButton.dataset.fallback || "/";
    const fallbackPath = (() => {
      try {
        return new URL(fallbackUrl, window.location.origin).pathname;
      } catch {
        return "/";
      }
    })();

    const hasSameOriginReferrer = (() => {
      try {
        return (
          document.referrer &&
          new URL(document.referrer).origin === window.location.origin
        );
      } catch {
        return false;
      }
    })();

    if (
      !hasSameOriginReferrer &&
      window.history.length <= 1 &&
      window.location.pathname === fallbackPath
    ) {
      backButton.disabled = true;
      backButton.classList.add("disabled");
      backButton.title = "No page to go back to";
    }

    backButton.addEventListener("click", () => {
      try {
        if (
          document.referrer &&
          new URL(document.referrer).origin === window.location.origin
        ) {
          window.history.back();
          return;
        }
      } catch {
        // ignore referrer parse errors
      }

      if (window.history.length > 1) {
        window.history.back();
        return;
      }

      window.location.assign(fallbackUrl);
    });
  }
});
