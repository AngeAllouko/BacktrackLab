"""Headless tests (no Tkinter needed)."""
import unittest

from queens.algorithm import solve_nqueens
from queens.rules import attacked_squares, attacker
from queens.theory import KNOWN_SOLUTIONS


def solutions(n, find_all=True):
    return [e["queens"] for e in solve_nqueens(n, find_all) if e["kind"] == "solution"]


class RuleTests(unittest.TestCase):
    def test_attacker(self):
        self.assertIsNone(attacker([], 0, 3))
        self.assertEqual(attacker([1], 1, 1), 0)        # same column
        self.assertEqual(attacker([1], 1, 2), 0)        # diagonal
        self.assertEqual(attacker([1], 1, 0), 0)        # other diagonal
        self.assertIsNone(attacker([1], 1, 3))          # safe knight-like jump

    def test_attacked_squares(self):
        sq = attacked_squares([1], 4)
        self.assertEqual(sq, {(1, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 1)})


class AlgorithmTests(unittest.TestCase):
    def test_known_solution_counts(self):
        for n in range(1, 9):
            self.assertEqual(len(solutions(n)), KNOWN_SOLUTIONS[n], f"N={n}")

    def test_first_solution_only(self):
        self.assertEqual(solutions(8, find_all=False), [[0, 4, 7, 5, 2, 6, 1, 3]])

    def test_solutions_are_valid_and_distinct(self):
        sols = solutions(7)
        self.assertEqual(len({tuple(s) for s in sols}), len(sols))
        for q in sols:
            self.assertEqual(sorted(q), list(range(7)))
            for i in range(7):
                for j in range(i + 1, 7):
                    self.assertNotEqual(abs(q[i] - q[j]), j - i)

    def test_every_backtrack_undoes_a_place(self):
        depth = 0
        for e in solve_nqueens(6, True):
            if e["kind"] == "place":
                depth += 1
            elif e["kind"] == "backtrack":
                depth -= 1
            self.assertGreaterEqual(depth, 0)
        self.assertEqual(depth, 0)


if __name__ == "__main__":
    unittest.main()
