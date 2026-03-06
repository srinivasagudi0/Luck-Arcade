const GAMES = {
  "Dice Roll": "dice",
  "Coin Flip": "coin",
  "Rock Paper Scissors": "rps",
  "Meteor Dodge": "meteor",
  "Planet Guess": "planet",
  "Number Guess": "guess",
};

const GAME_LABELS = Object.fromEntries(Object.entries(GAMES).map(([label, key]) => [key, label]));
const GAME_META = {
  "Dice Roll": { icon: "🎲", subtitle: "Pick a number and see if the die agrees with you.", tip: "One tap, one roll. Clean and quick." },
  "Coin Flip": { icon: "🪙", subtitle: "Call heads or tails and ride your luck.", tip: "Short rounds with instant result tracking." },
  "Rock Paper Scissors": { icon: "✊", subtitle: "One clean round against the computer.", tip: "Ties are neutral and do not affect win/loss stats." },
  "Meteor Dodge": { icon: "☄️", subtitle: "Choose your lane and avoid impact.", tip: "If the meteor lands in your lane, it is a loss." },
  "Planet Guess": { icon: "🪐", subtitle: "Scan the right orbit to lock onto the target.", tip: "Exact match wins. You get a higher/lower hint on misses." },
  "Number Guess": { icon: "🔢", subtitle: "Find the hidden number in three tries.", tip: "Misses give you a higher/lower hint before the next try." },
};

const GAME_PLAYBOOK = {
  "Dice Roll": [
    "Set your target number from 1 to 6.",
    "Press Roll once to launch the round.",
    "Match the roll to score a win.",
  ],
  "Coin Flip": [
    "Choose Heads or Tails.",
    "Flip once to resolve instantly.",
    "Matching side scores a win.",
  ],
  "Rock Paper Scissors": [
    "Choose Rock, Paper, or Scissors.",
    "Play one round against computer choice.",
    "Ties are neutral and not logged.",
  ],
  "Meteor Dodge": [
    "Pick your lane: Left, Center, or Right.",
    "Engage thrusters to reveal meteor lane.",
    "Avoid the meteor lane to win.",
  ],
  "Planet Guess": [
    "Scan an orbit from 1 to 8.",
    "Ping to compare your orbit with target.",
    "Exact orbit lock is a win.",
  ],
  "Number Guess": [
    "Pick a number from 1 to 10.",
    "Use higher/lower hints across 3 tries.",
    "Find the target before tries run out.",
  ],
};

const RULEBOOK = [
  "Dice Roll: win if your number matches the roll.",
  "Coin Flip: win if the coin matches your call.",
  "Rock Paper Scissors: ties are neutral and not logged as wins/losses.",
  "Meteor Dodge: win if your lane is different from the meteor lane.",
  "Planet Guess: win only on an exact orbit match.",
  "Number Guess: win by finding the number in 3 tries.",
];

const PERSIST_KEY = "luck_arcade_pages_stats";
const SESSION_KEY = "luck_arcade_pages_session";

function defaultStats() {
  const stats = { stats_total: 0 };
  Object.values(GAMES).forEach((game) => {
    stats[`stats_${game}_win`] = 0;
    stats[`stats_${game}_loss`] = 0;
  });
  return stats;
}

function defaultSession() {
  return {
    activeGame: "Dice Roll",
    dice_attempts: 0,
    coin_attempts: 0,
    rps_attempts: 0,
    meteor_attempts: 0,
    planet_attempts: 0,
    guess_attempts: 0,
    dice_history: [],
    coin_history: [],
    rps_history: [],
    meteor_history: [],
    planet_history: [],
    guess_history: [],
    activity_feed: [],
    guess_target: randInt(1, 10),
    guess_tries_left: 3,
    flash: null,
    controls: {
      dicePrediction: 3,
      coinChoice: "Heads",
      rpsChoice: "Rock",
      meteorLane: "Center",
      planetGuess: 4,
      numberGuess: 5,
      quickCommand: "",
    },
  };
}

function safeParse(raw, fallback) {
  try {
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function loadStats() {
  return { ...defaultStats(), ...safeParse(localStorage.getItem(PERSIST_KEY), {}) };
}

function saveStats(stats) {
  localStorage.setItem(PERSIST_KEY, JSON.stringify(stats));
}

function loadSession() {
  const base = defaultSession();
  const loaded = safeParse(sessionStorage.getItem(SESSION_KEY), {});
  return {
    ...base,
    ...loaded,
    controls: { ...base.controls, ...(loaded.controls || {}) },
  };
}

function saveSession() {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function wins(game) {
  return state.stats[`stats_${game}_win`];
}

function losses(game) {
  return state.stats[`stats_${game}_loss`];
}

function plays(game) {
  return wins(game) + losses(game);
}

function winRateNumber(game) {
  const total = plays(game);
  return total === 0 ? 0 : Math.round((wins(game) / total) * 100);
}

function winRate(game) {
  return `${winRateNumber(game)}%`;
}

function totalWins() {
  return Object.values(GAMES).reduce((sum, game) => sum + wins(game), 0);
}

function luckIndex() {
  return state.stats.stats_total === 0 ? "0%" : `${Math.round((totalWins() / state.stats.stats_total) * 100)}%`;
}

function bestGameSummary() {
  const played = Object.entries(GAMES)
    .map(([label, game]) => ({ label, rate: winRateNumber(game), rounds: plays(game) }))
    .filter((item) => item.rounds > 0);
  if (!played.length) return "No leading sector yet";
  played.sort((a, b) => (b.rate - a.rate) || (b.rounds - a.rounds));
  const top = played[0];
  return `Top sector: ${top.label} (${top.rate}% over ${top.rounds} rounds)`;
}

function setFlash(kind, title, detail, icon) {
  state.flash = { kind, title, detail, icon };
}

function recordResult(game, outcome, detail) {
  state.stats.stats_total += 1;
  state.stats[`stats_${game}_${outcome}`] += 1;
  saveStats(state.stats);

  const historyKey = `${game}_history`;
  state[historyKey] = [detail, ...(state[historyKey] || [])].slice(0, 25);
  const label = GAME_LABELS[game];
  const icon = GAME_META[label].icon;
  const tag = outcome === "win" ? "WIN" : "LOSS";
  state.activity_feed = [`${icon} ${label}: ${detail} [${tag}]`, ...state.activity_feed].slice(0, 30);
}

function resetSessionState() {
  const activeGame = state.activeGame;
  state = defaultSession();
  state.activeGame = activeGame;
  setFlash("neutral", "Session reset", "Saved totals are still available in this browser.", "⌨️");
  saveSession();
}

function handleQuickCommand(command) {
  const text = command.trim();
  if (!text) {
    setFlash("neutral", "Quick Command", "Enter a command to run.", "⌨️");
    return;
  }
  const value = text.toLowerCase();
  if (value === "help" || value === "h" || value === "?" || value === "info" || value === "instructions") {
    setFlash("neutral", "Quick Command", "Try: help, stats, reset", "⌨️");
    return;
  }
  if (value === "stats" || value === "stat" || value === "score" || value === "scores") {
    setFlash("neutral", "Saved totals", `Total plays: ${state.stats.stats_total} | Wins: ${totalWins()} | Luck index: ${luckIndex()}`, "⌨️");
    return;
  }
  if (value === "reset" || value === "clear") {
    resetSessionState();
    return;
  }
  if (["menu", "m", "main menu", "home", "back", "quit", "exit", "q", "stop", "end"].includes(value)) {
    setFlash("loss", "Quick Command", `'${text}' is not used here. Use the game menu.`, "⌨️");
    return;
  }
  setFlash("loss", "Quick Command", `Unknown command: '${text}'. Try 'help'.`, "⌨️");
}

function handleGameAction() {
  const game = GAMES[state.activeGame];
  if (game === "dice") {
    const prediction = Number(state.controls.dicePrediction);
    state.dice_attempts += 1;
    const roll = randInt(1, 6);
    const outcome = roll === prediction ? "win" : "loss";
    recordResult("dice", outcome, `Predicted ${prediction}, rolled ${roll}`);
    if (outcome === "win") {
      setFlash("win", `Rolled ${roll}`, "Perfect call. You matched the die.", "🎲");
    } else {
      setFlash("loss", `Rolled ${roll}`, `You predicted ${prediction}. Queue up another round.`, "🎲");
    }
    return;
  }

  if (game === "coin") {
    const choice = state.controls.coinChoice;
    state.coin_attempts += 1;
    const result = Math.random() < 0.5 ? "Heads" : "Tails";
    const outcome = result === choice ? "win" : "loss";
    recordResult("coin", outcome, `Called ${choice}, got ${result}`);
    if (outcome === "win") {
      setFlash("win", `Coin landed ${result}`, "Clean read on the flip.", "🪙");
    } else {
      setFlash("loss", `Coin landed ${result}`, `You called ${choice}. Try a quick rematch.`, "🪙");
    }
    return;
  }

  if (game === "rps") {
    const userChoice = state.controls.rpsChoice;
    state.rps_attempts += 1;
    const choices = ["Rock", "Paper", "Scissors"];
    const compChoice = choices[randInt(0, choices.length - 1)];
    const beats = { Rock: "Scissors", Paper: "Rock", Scissors: "Paper" };
    if (userChoice === compChoice) {
      setFlash("neutral", "Tie round", `You: ${userChoice} | Computer: ${compChoice}`, "✊");
      return;
    }
    const outcome = beats[userChoice] === compChoice ? "win" : "loss";
    const detail = `You: ${userChoice} | Computer: ${compChoice}`;
    recordResult("rps", outcome, detail);
    setFlash(outcome, outcome === "win" ? "You won the round" : "Computer won the round", detail, "✊");
    return;
  }

  if (game === "meteor") {
    const lane = state.controls.meteorLane;
    state.meteor_attempts += 1;
    const choices = ["Left", "Center", "Right"];
    const incoming = choices[randInt(0, choices.length - 1)];
    const outcome = incoming === lane ? "loss" : "win";
    recordResult("meteor", outcome, `Lane: ${lane} | Meteor: ${incoming}`);
    if (outcome === "win") {
      setFlash("win", "Safe passage", `Meteor crossed ${incoming}. You chose ${lane}.`, "☄️");
    } else {
      setFlash("loss", "Direct hit", `Meteor crossed ${incoming}. You chose ${lane}.`, "☄️");
    }
    return;
  }

  if (game === "planet") {
    const guess = Number(state.controls.planetGuess);
    state.planet_attempts += 1;
    const target = randInt(1, 8);
    const outcome = target === guess ? "win" : "loss";
    recordResult("planet", outcome, `Guessed ${guess}, target was ${target}`);
    if (outcome === "win") {
      setFlash("win", "Target located", `Orbit ${guess} was the correct scan.`, "🪐");
    } else {
      const hint = target > guess ? "higher" : "lower";
      setFlash("neutral", `Not orbit ${guess}`, `Hint from scan: go ${hint}.`, "🪐");
    }
    return;
  }

  if (game === "guess") {
    const guess = Number(state.controls.numberGuess);
    state.guess_attempts += 1;
    if (guess === state.guess_target) {
      const used = 4 - state.guess_tries_left;
      const suffix = used === 1 ? "" : "s";
      recordResult("guess", "win", `Guessed ${guess} correctly in ${used} attempt${suffix}`);
      setFlash("win", "Correct guess", `It was ${state.guess_target}. Solved in ${used} attempt${suffix}.`, "🔢");
      state.guess_target = randInt(1, 10);
      state.guess_tries_left = 3;
      return;
    }

    state.guess_tries_left -= 1;
    if (state.guess_tries_left <= 0) {
      recordResult("guess", "loss", `Missed 3 tries, target was ${state.guess_target}`);
      setFlash("loss", "Out of tries", `The number was ${state.guess_target}. Fresh round loaded.`, "🔢");
      state.guess_target = randInt(1, 10);
      state.guess_tries_left = 3;
    } else {
      const hint = state.guess_target > guess ? "higher" : "lower";
      setFlash("neutral", "Keep scanning", `Try ${hint}. Tries left: ${state.guess_tries_left}.`, "🔢");
    }
  }
}

function resetNumberRound() {
  state.guess_target = randInt(1, 10);
  state.guess_tries_left = 3;
  setFlash("neutral", "Round reset", "Started a fresh number puzzle.", "🔢");
}

function attachEvents() {
  document.querySelectorAll("[data-game-select]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeGame = button.dataset.gameSelect;
      state.flash = null;
      saveSession();
      render();
    });
  });

  const resetSessionButton = document.querySelector("#reset-session");
  if (resetSessionButton) {
    resetSessionButton.addEventListener("click", () => {
      resetSessionState();
      render();
    });
  }

  document.querySelectorAll("[data-command]").forEach((button) => {
    button.addEventListener("click", () => {
      handleQuickCommand(button.dataset.command || "");
      state.controls.quickCommand = "";
      saveSession();
      render();
    });
  });

  const commandForm = document.querySelector("#command-form");
  if (commandForm) {
    commandForm.addEventListener("submit", (event) => {
      event.preventDefault();
      handleQuickCommand(state.controls.quickCommand);
      state.controls.quickCommand = "";
      saveSession();
      render();
    });
  }

  document.querySelectorAll("[data-control]").forEach((input) => {
    const control = input.dataset.control;
    input.addEventListener("input", () => {
      state.controls[control] = input.type === "range" ? Number(input.value) : input.value;
      saveSession();
      if (input.nextElementSibling && input.nextElementSibling.tagName === "OUTPUT") {
        input.nextElementSibling.value = input.value;
      }
    });
    input.addEventListener("change", () => {
      state.controls[control] = input.type === "range" ? Number(input.value) : input.value;
      saveSession();
    });
  });

  const gameForm = document.querySelector("#game-form");
  if (gameForm) {
    gameForm.addEventListener("submit", (event) => {
      event.preventDefault();
      handleGameAction();
      saveSession();
      render();
    });
  }

  const resetGuessButton = document.querySelector("#reset-number-round");
  if (resetGuessButton) {
    resetGuessButton.addEventListener("click", () => {
      resetNumberRound();
      saveSession();
      render();
    });
  }
}

function gameFormMarkup() {
  const key = GAMES[state.activeGame];
  const controls = state.controls;

  if (key === "dice") {
    return `
      <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
      <form id="game-form" class="game-form">
        <label for="dicePrediction">Your prediction</label>
        <input id="dicePrediction" data-control="dicePrediction" type="range" min="1" max="6" value="${controls.dicePrediction}">
        <output>${controls.dicePrediction}</output>
        <button class="button" type="submit">Roll the die</button>
      </form>`;
  }

  if (key === "coin") {
    return `
      <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
      <form id="game-form" class="game-form">
        <label>Your call</label>
        <div class="segmented">
          ${["Heads", "Tails"].map((choice) => `
            <label>
              <input data-control="coinChoice" type="radio" name="coinChoice" value="${choice}" ${controls.coinChoice === choice ? "checked" : ""}>
              <span>${choice}</span>
            </label>`).join("")}
        </div>
        <button class="button" type="submit">Flip coin</button>
      </form>`;
  }

  if (key === "rps") {
    return `
      <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
      <form id="game-form" class="game-form">
        <label>Your choice</label>
        <div class="segmented triple">
          ${["Rock", "Paper", "Scissors"].map((choice) => `
            <label>
              <input data-control="rpsChoice" type="radio" name="rpsChoice" value="${choice}" ${controls.rpsChoice === choice ? "checked" : ""}>
              <span>${choice}</span>
            </label>`).join("")}
        </div>
        <button class="button" type="submit">Play</button>
      </form>`;
  }

  if (key === "meteor") {
    return `
      <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
      <form id="game-form" class="game-form">
        <label>Your lane</label>
        <div class="segmented triple">
          ${["Left", "Center", "Right"].map((choice) => `
            <label>
              <input data-control="meteorLane" type="radio" name="meteorLane" value="${choice}" ${controls.meteorLane === choice ? "checked" : ""}>
              <span>${choice}</span>
            </label>`).join("")}
        </div>
        <button class="button" type="submit">Engage thrusters</button>
      </form>`;
  }

  if (key === "planet") {
    return `
      <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
      <form id="game-form" class="game-form">
        <label for="planetGuess">Your scan orbit</label>
        <input id="planetGuess" data-control="planetGuess" type="range" min="1" max="8" value="${controls.planetGuess}">
        <output>${controls.planetGuess}</output>
        <button class="button" type="submit">Ping the planet</button>
      </form>`;
  }

  return `
    <p class="game-tip">${GAME_META[state.activeGame].tip}</p>
    <form id="game-form" class="game-form">
      <p class="sidebar-copy">Tries left in current round: ${state.guess_tries_left}</p>
      <label for="numberGuess">Your guess</label>
      <input id="numberGuess" data-control="numberGuess" type="range" min="1" max="10" value="${controls.numberGuess}">
      <output>${controls.numberGuess}</output>
      <button class="button" type="submit">Submit guess</button>
    </form>
    <button id="reset-number-round" class="button button-secondary" type="button">Reset number round</button>`;
}

function render() {
  const activeKey = GAMES[state.activeGame];
  const activeMeta = GAME_META[state.activeGame];
  const history = state[`${activeKey}_history`] || [];
  const statCards = [
    ["Total rounds", state.stats.stats_total, "Across all games"],
    ["Total wins", totalWins(), "Across all games"],
    ["Win rate", luckIndex(), "Across all games"],
    ["Dice Roll", `${wins("dice")}W / ${losses("dice")}L`, `${winRate("dice")} WR`],
    ["Coin Flip", `${wins("coin")}W / ${losses("coin")}L`, `${winRate("coin")} WR`],
    ["RPS", `${wins("rps")}W / ${losses("rps")}L`, `${winRate("rps")} WR`],
    ["Meteor", `${wins("meteor")}W / ${losses("meteor")}L`, `${winRate("meteor")} WR`],
    ["Planet", `${wins("planet")}W / ${losses("planet")}L`, `${winRate("planet")} WR`],
    ["Number Guess", `${wins("guess")}W / ${losses("guess")}L`, `${winRate("guess")} WR`],
  ];

  document.querySelector("#app").innerHTML = `
    <div class="app-shell">
      <aside class="sidebar panel">
        <div>
          <h2>Game Menu</h2>
          <p class="sidebar-copy">Rounds ${state.stats.stats_total} | Wins ${totalWins()} | Win rate ${luckIndex()}</p>
        </div>

        <nav class="game-nav">
          ${Object.keys(GAMES).map((label) => `
            <button class="selector-card ${label === state.activeGame ? "active" : ""}" data-game-select="${label}">
              <div class="selector-row">
                <p class="selector-title">${GAME_META[label].icon} ${label}</p>
                <span class="selector-rate">Win ${winRate(GAMES[label])}</span>
              </div>
              <p class="selector-sub">${GAME_META[label].subtitle}</p>
            </button>`).join("")}
        </nav>

        <div class="sidebar-section">
          <h3>Session Controls</h3>
          <button id="reset-session" class="button button-secondary full" type="button">Reset session</button>
          <p class="sidebar-note">Clears local attempts and round history while preserving saved totals in this browser.</p>
        </div>

        <div class="sidebar-section quick-panel">
          <h3>Quick Command</h3>
          <p class="sidebar-copy">Use a shortcut button or type a command. Try <code>help</code>, <code>stats</code>, or <code>reset</code>.</p>
          <div class="quick-grid">
            <button class="button full" type="button" data-command="help">Help</button>
            <button class="button full" type="button" data-command="stats">Stats</button>
            <button class="button button-secondary full" type="button" data-command="reset">Reset</button>
          </div>
          <form id="command-form" class="command-form">
            <input data-control="quickCommand" type="text" value="${state.controls.quickCommand}" placeholder="help, stats, reset">
            <button class="button full" type="submit">Run command</button>
          </form>
          <p class="note-line">GitHub Pages build note: browser storage replaces Flask sessions and <code>stats.json</code>.</p>
        </div>
      </aside>

      <main class="main-content">
        <section class="hero panel">
          <p class="hero-kicker">Luck Arcade</p>
          <h1 class="hero-title">Arcade Hub</h1>
          <p class="hero-copy">Quick mini-games with instant results. Active game: <strong>${activeMeta.icon} ${state.activeGame}</strong> - ${activeMeta.subtitle}</p>
          <div class="hero-row">
            <span class="hero-chip">Rounds: ${state.stats.stats_total}</span>
            <span class="hero-chip">Wins: ${totalWins()}</span>
            <span class="hero-chip">Win rate: ${luckIndex()}</span>
            <span class="hero-chip">Games: ${Object.keys(GAMES).length}</span>
            <span class="hero-chip">${bestGameSummary()}</span>
          </div>
        </section>

        <section class="stats-grid">
          ${statCards.map(([label, value, subtext]) => `
            <article class="metric-card">
              <p class="metric-label">${label}</p>
              <p class="metric-value">${value}</p>
              <p class="metric-subtext">${subtext}</p>
            </article>`).join("")}
        </section>

        <div class="two-col section-gap">
          <section class="brief-card panel">
            <p class="brief-kicker">How to play</p>
            <p class="brief-title">${activeMeta.icon} ${state.activeGame}</p>
            <ol class="brief-list">
              ${GAME_PLAYBOOK[state.activeGame].map((step) => `<li>${step}</li>`).join("")}
            </ol>
          </section>

          <section class="panel info-panel">
            <h3>Mission Notes</h3>
            <p class="sidebar-copy">This GitHub Pages version keeps the same arcade flow, but persistence is browser-local because Pages is static hosting.</p>
          </section>
        </div>

        <section class="panel game-panel">
          <div class="game-heading">
            <div class="game-icon">${activeMeta.icon}</div>
            <div>
              <h2 class="game-title">${state.activeGame}</h2>
              <p class="game-subtitle">${activeMeta.subtitle}</p>
            </div>
          </div>

          ${state.flash ? `
            <div class="result-banner result-${state.flash.kind}">
              <p class="result-top">${state.flash.icon} ${state.flash.title}</p>
              <p class="result-text">${state.flash.detail}</p>
            </div>` : ""}

          <div class="two-col game-layout">
            <section>
              ${gameFormMarkup()}
            </section>

            <section class="side-metrics">
              <article class="metric-card accent">
                <p class="metric-label">Total attempts</p>
                <p class="metric-value">${state[`${activeKey}_attempts`]}</p>
              </article>
              ${activeKey === "guess" ? `
                <article class="metric-card accent">
                  <p class="metric-label">Tries left</p>
                  <p class="metric-value">${state.guess_tries_left}</p>
                </article>` : ""}
              <article class="history-card">
                <p class="history-title">Recent Rounds: ${state.activeGame}</p>
                ${history.length ? `<ul>${history.slice(0, 8).map((item) => `<li>${item}</li>`).join("")}</ul>` : `<p class="history-empty">No rounds yet. Play once and this fills up.</p>`}
              </article>
            </section>
          </div>
        </section>

        <div class="two-col section-gap">
          <section class="feed-card panel">
            <p class="feed-title">Flight Log</p>
            ${state.activity_feed.length ? state.activity_feed.slice(0, 8).map((item) => `<div class="feed-item">${item}</div>`).join("") : '<p class="history-empty">No rounds recorded yet. Play any sector to start the log.</p>'}
          </section>

          <section class="rulebook panel">
            <p class="rulebook-title">Starboard Rules</p>
            <p class="rulebook-copy">Every mission logs to your stats and flight log. Keep this nearby when switching sectors.</p>
            <ul class="rulebook-list">
              ${RULEBOOK.map((item) => `<li>${item}</li>`).join("")}
            </ul>
          </section>
        </div>
      </main>
    </div>`;

  saveSession();
  attachEvents();
}

let state = {
  stats: loadStats(),
  ...loadSession(),
};

render();
