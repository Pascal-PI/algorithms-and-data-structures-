# Matchmaking Algorithm

`matchmakingalgorithm.py` matches queued players using their ratings and wait times.

## Rules

- Players are considered in queue age order (`joined_at`), with `user_id` breaking
  ties. Each unmatched player gets one turn to find an opponent.
- An opponent is eligible when the rating difference is no greater than the
  current player's allowed gap. The gap starts at 100, grows by 50 every 30
  seconds waited, and is capped at 400. Negative wait times are treated as zero.
- Among eligible opponents, the smallest rating difference wins. Ties go to the
  opponent who joined earlier, then to the lexically smaller `user_id`.
- Matched players are removed from the queue. Players with no eligible opponent
  are returned in `waiting`, in queue age order.

## Complexity

The implementation sorts the queue and builds a heap for each rating, taking
`O(n log n)` time and `O(n)` space for `n` players. For each player it probes
integer rating differences from zero through the allowed gap `G` (at most 400),
and lazily removes inactive heap entries. This takes `O(nG + n log n)` total
time; since `G` is capped at 400, it scales as `O(n log n)` with queue size.

## Tests and benchmark

Run the unit tests with:

```sh
python -m unittest discover -s tests
```

Run the benchmark against a simple `O(n^2)` reference implementation with:

```sh
python benchmarks/benchmark_matchmaking.py
```

The benchmark reports median runtime over five runs for deterministic queues
of 100, 500, 1,000, and 2,000 players.
