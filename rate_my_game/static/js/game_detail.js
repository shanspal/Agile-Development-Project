document.addEventListener("DOMContentLoaded", () => {
  const config = window.RMG_DETAIL_CONFIG;

  const ratingForm = document.getElementById("rating-form");
  const gameplayInput = document.getElementById("gameplay-input");
  const difficultyInput = document.getElementById("difficulty-input");
  const ratingMessage = document.getElementById("rating-message");

  const avgGameplayEl = document.getElementById("avg-gameplay");
  const avgDifficultyEl = document.getElementById("avg-difficulty");
  const ratingsCountEl = document.getElementById("ratings-count");

  const tagsContainer = document.getElementById("tags-container");

  async function fetchTags() {
    const res = await fetch(config.apiTagsUrl);
    if (!res.ok) {
      console.error("Failed to fetch tags");
      return;
    }
    const tags = await res.json();
    renderTags(tags);
  }

  function renderTags(tags) {
    tagsContainer.innerHTML = "";
    const maxCount = tags.reduce((max, t) => Math.max(max, t.count), 0) || 1;

    tags.forEach((tag) => {
      const row = document.createElement("div");
      row.className = "tag-row";

      const label = document.createElement("button");
      label.type = "button";
      label.className = "btn btn-outline-secondary btn-sm tag-label";
      label.textContent = tag.tag_name;
      label.addEventListener("click", () => voteTag(tag.tag_name));

      const barWrapper = document.createElement("div");
      barWrapper.className = "tag-bar-wrapper";

      const barFill = document.createElement("div");
      barFill.className = "tag-bar-fill";
      const percentage = (tag.count / maxCount) * 100;
      barFill.style.width = `${percentage}%`;

      barWrapper.appendChild(barFill);

      const count = document.createElement("div");
      count.className = "tag-count text-muted";
      count.textContent = tag.count;

      row.appendChild(label);
      row.appendChild(barWrapper);
      row.appendChild(count);

      tagsContainer.appendChild(row);
    });
  }

  async function voteTag(tagName) {
    const url = config.apiTagVoteUrlTemplate.replace(
      "__TAG__",
      encodeURIComponent(tagName),
    );
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      console.error("Failed to vote tag");
      return;
    }
    await res.json();
    fetchTags();
  }

  ratingForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    ratingMessage.textContent = "";
    ratingMessage.className = "small";

    const gameplay = gameplayInput.value;
    const difficulty = difficultyInput.value;

    if (!gameplay || !difficulty) {
      ratingMessage.textContent = "Please select both gameplay and difficulty.";
      ratingMessage.classList.add("text-danger");
      return;
    }

    const res = await fetch(config.apiRatingsUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        gameplay: gameplay,
        difficulty: difficulty,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      ratingMessage.textContent = err.error || "Failed to submit rating.";
      ratingMessage.classList.add("text-danger");
      return;
    }

    const data = await res.json();
    avgGameplayEl.textContent = data.avg_gameplay
      ? data.avg_gameplay.toFixed(1)
      : "-";
    avgDifficultyEl.textContent = data.avg_difficulty
      ? data.avg_difficulty.toFixed(1)
      : "-";
    ratingsCountEl.textContent = data.ratings_count;

    ratingMessage.textContent = "Thanks for your rating!";
    ratingMessage.classList.add("text-success");

    ratingForm.reset();
  });

  // Initial load
  fetchTags();
});
