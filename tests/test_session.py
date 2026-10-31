import unittest

from queens.algorithm import solve_nqueens
from queens.session import Session


def run_to_end(s):
    while s.forward() is not None:
        pass


class SessionTests(unittest.TestCase):
    def test_stats_and_summary(self):
        s = Session(solve_nqueens(4, True))
        run_to_end(s)
        _, stats = s.current
        self.assertEqual(stats["solutions"], 2)
        self.assertGreater(stats["rejects"], 0)
        self.assertGreater(stats["backtracks"], 0)
        self.assertIn("2 solution", s.summary(4))
        self.assertIn("no solution", Session(iter(())).summary(3))

    def test_back_and_forward_replay(self):
        s = Session(solve_nqueens(4, True))
        first = [s.forward() for _ in range(10)]
        for _ in range(5):
            self.assertTrue(s.back())
        self.assertEqual(s.current[0], first[4])
        self.assertEqual(s.forward(), first[5])         # replayed, not recomputed
        self.assertEqual(s.current[1]["steps"], 6)

    def test_back_to_empty_board(self):
        s = Session(solve_nqueens(4, True))
        s.forward()
        self.assertTrue(s.back())
        self.assertEqual(s.current, (None, {"steps": 0, "rejects": 0, "backtracks": 0, "solutions": 0}))
        self.assertFalse(s.back())

    def test_going_back_unfinds_solutions(self):
        s = Session(solve_nqueens(4, True))
        while s.forward()["kind"] != "solution":
            pass
        self.assertEqual(len(s.solutions_so_far()), 1)
        s.back()
        self.assertEqual(len(s.solutions_so_far()), 0)


if __name__ == "__main__":
    unittest.main()
