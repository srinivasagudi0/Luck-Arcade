import json
from pathlib import Path

GAMES = ("dice", "coin", "rps", "meteor", "planet", 'guess')


def default_stats() -> dict:
    data = {"stats_total": 0}
    for game in GAMES:
        data[f"stats_{game}_win"] = 0
        data[f"stats_{game}_loss"] = 0
    return data


def load_stats(storage_path: str = "stats.json") -> dict:
    path = Path(storage_path)
    defaults = default_stats()
    if not path.exists():
        return defaults
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return defaults
    if not isinstance(payload, dict):
        return defaults

    merged = defaults.copy()
    for key in merged:
        value = payload.get(key, merged[key])
        merged[key] = value if isinstance(value, int) and value >= 0 else merged[key]
    return merged


def save_stats(data: dict, storage_path: str = "stats.json") -> dict:
    path = Path(storage_path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def update_and_persist_stats(game: str, result: str, *, storage_path: str = "stats.json") -> dict:
    if game not in GAMES:
        raise ValueError(f"Unsupported game: {game}")
    if result not in ("win", "loss"):
        raise ValueError(f"Unsupported result: {result}")

    stats = load_stats(storage_path)
    stats["stats_total"] += 1
    stats[f"stats_{game}_{result}"] += 1
    return save_stats(stats, storage_path)


def format_stats_summary(stats: dict) -> str:
    lines = [f"Total plays: {stats['stats_total']}"]
    for game in GAMES:
        wins = stats[f"stats_{game}_win"]
        losses = stats[f"stats_{game}_loss"]
        lines.append(f"{game}: {wins}W/{losses}L")
    return "\n".join(lines)
