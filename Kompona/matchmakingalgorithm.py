# Match Making Algorithm

from dataclasses import dataclass
from heapq import heapify, heappop

@dataclass(frozen=True)
class Player:
    user_id: str
    rating: int
    joined_at: int

def allowed_gap(wait_seconds):
    return min(400, 100 + (wait_seconds // 30) * 50)

def match_players(queue, now):
    """
    Returns:
      matches: list of (user_id, user_id)
      waiting: list of unmatched user_ids

    Oldest players get first priority.
    Choose the eligible opponent with the
    closest rating. Break ties by queue age,
    then user_id.
    """
    matches = []
    waiting = []

    ordered = sorted(queue, key=lambda player: (player.joined_at, player.user_id))
    active = [True] * len(ordered)
    by_rating = {}
    for i, player in enumerate(ordered):
        by_rating.setdefault(player.rating, []).append(
            (player.joined_at, player.user_id, i)
        )
    for players in by_rating.values():
        heapify(players)

    for i, player in enumerate(ordered):
        if not active[i]:
            continue
        active[i] = False

        gap = allowed_gap(max(0, now - player.joined_at))
        best_index = None
        for rating_gap in range(gap + 1):
            candidates = []
            ratings = (player.rating,) if rating_gap == 0 else (
                player.rating - rating_gap,
                player.rating + rating_gap,
            )
            for rating in ratings:
                heap = by_rating.get(rating)
                if heap is None:
                    continue
                while heap and not active[heap[0][2]]:
                    heappop(heap)
                if heap:
                    candidates.append(heap[0])
            if candidates:
                best_index = min(candidates)[2]
                break

        if best_index is not None:
            active[best_index] = False
            matches.append((player.user_id, ordered[best_index].user_id))
        else:
            waiting.append(player.user_id)

    return matches, waiting
