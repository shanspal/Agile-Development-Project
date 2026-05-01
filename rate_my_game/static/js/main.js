document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const companyInput = document.getElementById("company-input");
  const sortSelect = document.getElementById("sort-select");
  const tagButtons = document.querySelectorAll(".tag-filter-btn");
  const searchForm = document.getElementById("search-form");
  const clearBtn = document.getElementById("clear-filters");

  const tableBody = document.querySelector("#games-table tbody");
  const cardsContainer = document.getElementById("games-cards");
  const noResults = document.getElementById("no-results");

  let activeTags = new Set();

  function getSelectedTags() {
    return Array.from(activeTags);
  }

  function buildQueryParams() {
    const params = new URLSearchParams();
    if (searchInput.value.trim())
      params.append("search", searchInput.value.trim());
    if (companyInput.value.trim())
      params.append("company", companyInput.value.trim());
    params.append("sort", sortSelect.value);
    getSelectedTags().forEach((tag) => params.append("tags", tag));
    return params.toString();
  }

  async function fetchGames() {
    const url = `${window.RMG_CONFIG.apiGamesUrl}?${buildQueryParams()}`;
    const res = await fetch(url);
    if (!res.ok) {
      console.error("Failed to fetch games");
      return;
    }
    const data = await res.json();
    renderGames(data);
  }

  function renderGames(games) {
    tableBody.innerHTML = "";
    cardsContainer.innerHTML = "";

    if (!games.length) {
      noResults.classList.remove("d-none");
      return;
    }
    noResults.classList.add("d-none");

    games.forEach((game) => {
      const detailUrl = `${window.RMG_CONFIG.gameDetailBaseUrl}${game.id}`;

      // Table row (desktop)
      const tr = document.createElement("tr");

      const nameTd = document.createElement("td");
      nameTd.textContent = game.name;

      const companyTd = document.createElement("td");
      companyTd.textContent = game.company;

      const gameplayTd = document.createElement("td");
      gameplayTd.classList.add("text-center");
      gameplayTd.textContent = game.avg_gameplay
        ? game.avg_gameplay.toFixed(1)
        : "-";

      const difficultyTd = document.createElement("td");
      difficultyTd.classList.add("text-center");
      difficultyTd.textContent = game.avg_difficulty
        ? game.avg_difficulty.toFixed(1)
        : "-";

      const countTd = document.createElement("td");
      countTd.classList.add("text-center");
      countTd.textContent = game.ratings_count;

      const actionsTd = document.createElement("td");
      actionsTd.classList.add("text-center");
      const viewBtn = document.createElement("a");
      viewBtn.href = detailUrl;
      viewBtn.className = "btn btn-sm btn-outline-primary";
      viewBtn.textContent = "View";
      actionsTd.appendChild(viewBtn);

      tr.appendChild(nameTd);
      tr.appendChild(companyTd);
      tr.appendChild(gameplayTd);
      tr.appendChild(difficultyTd);
      tr.appendChild(countTd);
      tr.appendChild(actionsTd);

      tableBody.appendChild(tr);

      // Card (mobile)
      const card = document.createElement("div");
      card.className = "game-card";

      const title = document.createElement("div");
      title.className = "game-card-title";
      title.textContent = game.name;

      const company = document.createElement("div");
      company.className = "game-card-company";
      company.textContent = game.company;

      const ratings = document.createElement("div");
      ratings.className = "game-card-ratings mt-1";
      ratings.innerHTML = `
                Gameplay: <strong>${game.avg_gameplay ? game.avg_gameplay.toFixed(1) : "-"}</strong> &middot;
                Difficulty: <strong>${game.avg_difficulty ? game.avg_difficulty.toFixed(1) : "-"}</strong><br>
                Ratings: <strong>${game.ratings_count}</strong>
            `;

      const actions = document.createElement("div");
      actions.className = "mt-2";
      const viewBtnMobile = document.createElement("a");
      viewBtnMobile.href = detailUrl;
      viewBtnMobile.className = "btn btn-sm btn-outline-primary";
      viewBtnMobile.textContent = "View Details";
      actions.appendChild(viewBtnMobile);

      card.appendChild(title);
      card.appendChild(company);
      card.appendChild(ratings);
      card.appendChild(actions);

      cardsContainer.appendChild(card);
    });
  }

  // Tag filter buttons
  tagButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tag = btn.dataset.tag;
      if (activeTags.has(tag)) {
        activeTags.delete(tag);
        btn.classList.remove("active");
      } else {
        activeTags.add(tag);
        btn.classList.add("active");
      }
    });
  });

  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    fetchGames();
  });

  clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    companyInput.value = "";
    sortSelect.value = "gameplay_desc";
    activeTags.clear();
    tagButtons.forEach((btn) => btn.classList.remove("active"));
    fetchGames();
  });

  // Initial load
  fetchGames();
});
