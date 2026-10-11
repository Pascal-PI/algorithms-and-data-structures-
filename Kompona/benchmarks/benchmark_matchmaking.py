"""Compare matchmaking with a straightforward quadratic reference version."""

from pathlib import Path
import random
import statistics
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from matchmakingalgorithm import Player, match_players


def quadratic_match_players(queue, now):
    """Reference implementation with a full candidate scan per player."""
    ordered = sorted(queue, key=lambda player: (player.joined_at, player.user_id))
    matched = [False] * len(ordered)
    matches = []
    waiting = []

    for i, player in enumerate(ordered):
        if matched[i]:
            continue
        gap = min(400, 100 + (max(0, now - player.joined_at) // 30) * 50)
        best = None
        for j, opponent in enumerate(ordered):
            if i == j or matched[j]:
                continue
            rating_gap = abs(player.rating - opponent.rating)
            if rating_gap <= gap:
                key = (rating_gap, opponent.joined_at, opponent.user_id)
                if best is None or key < best[0]:
                    best = (key, j)
        if best is None:
            matched[i] = True
            waiting.append(player.user_id)
        else:
            j = best[1]
            matched[i] = matched[j] = True
            matches.append((player.user_id, ordered[j].user_id))

    return matches, waiting


def make_queue(size, seed=20261011):
    rng = random.Random(seed)
    return [
        Player(f"player-{i:06d}", rng.randrange(800, 2401), rng.randrange(0, 3600))
        for i in range(size)
    ]


def median_runtime(function, queue, now, repeats):
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        function(queue, now)
        samples.append(perf_counter() - start)
    return statistics.median(samples)


def main():
    sizes = (100, 500, 1000, 2000)
    repeats = 5
    print(f"Median runtime over {repeats} runs (milliseconds)")
    print(f"{'players':>8} {'bucket/heap':>14} {'quadratic':>12} {'speedup':>9}")
    for size in sizes:
        queue = make_queue(size)
        if match_players(queue, 3600) != quadratic_match_players(queue, 3600):
            raise AssertionError(f"Implementations differ for queue size {size}")
        optimized = median_runtime(match_players, queue, 3600, repeats)
        quadratic = median_runtime(quadratic_match_players, queue, 3600, repeats)
        print(
            f"{size:8d} {optimized * 1000:14.3f} {quadratic * 1000:12.3f} "
            f"{quadratic / optimized:8.2f}x"
        )


if __name__ == "__main__":
    main()
