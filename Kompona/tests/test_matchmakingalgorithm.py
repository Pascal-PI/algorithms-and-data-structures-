import unittest

from matchmakingalgorithm import Player, match_players


class MatchPlayersTests(unittest.TestCase):
    def test_equal_ratings_are_matched(self):
        queue = [
            Player("first", 1200, 10),
            Player("second", 1200, 20),
        ]

        self.assertEqual(match_players(queue, now=30), ([('first', 'second')], []))

    def test_rating_gap_tie_prefers_older_then_user_id(self):
        queue = [
            Player("target", 1000, 0),
            Player("older", 900, 10),
            Player("newer", 1100, 20),
        ]

        self.assertEqual(
            match_players(queue, now=30),
            ([('target', 'older')], ['newer']),
        )

    def test_user_id_breaks_equal_age_and_rating_ties(self):
        queue = [
            Player("target", 1000, 0),
            Player("zeta", 1000, 10),
            Player("alpha", 1000, 10),
        ]

        self.assertEqual(
            match_players(queue, now=30),
            ([('target', 'alpha')], ['zeta']),
        )

    def test_empty_queue(self):
        self.assertEqual(match_players([], now=100), ([], []))

    def test_players_outside_allowed_rating_gap_wait(self):
        queue = [
            Player("low", 1000, 90),
            Player("high", 1151, 90),
        ]

        self.assertEqual(match_players(queue, now=100), ([], ['high', 'low']))


if __name__ == "__main__":
    unittest.main()
