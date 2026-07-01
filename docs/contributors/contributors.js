(() => {
  const game = document.querySelector("[data-egg-game]");
  if (!game) {
    return;
  }

  const scoreOutput = game.querySelector("[data-score]");
  const missesOutput = game.querySelector("[data-misses]");
  let score = 0;
  let misses = 0;

  game.addEventListener("click", (event) => {
    const egg = event.target.closest(".egg");
    if (!egg || egg.classList.contains("collected")) {
      return;
    }

    if (egg.dataset.target === "true") {
      score += 1;
      egg.classList.add("collected");
    } else {
      misses += 1;
      egg.animate(
        [
          { transform: "translateX(0)" },
          { transform: "translateX(-0.4rem)" },
          { transform: "translateX(0.4rem)" },
          { transform: "translateX(0)" },
        ],
        { duration: 220, easing: "ease-out" },
      );
    }

    scoreOutput.textContent = String(score);
    missesOutput.textContent = String(misses);
  });
})();
