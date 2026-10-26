"""Unit tests for the add() and sub() functions in main.py."""

import unittest

from main import add, sub


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertAlmostEqual(add(1.5, 2.25), 3.75)

    def test_negative_numbers(self):
        self.assertAlmostEqual(add(-1.5, -2.5), -4.0)

    def test_mixed_signs(self):
        self.assertAlmostEqual(add(10.0, -4.5), 5.5)

    def test_zero(self):
        self.assertEqual(add(0.0, 0.0), 0.0)
        self.assertAlmostEqual(add(7.25, 0.0), 7.25)

    def test_floating_point_rounding(self):
        # 0.1 + 0.2 is not exactly 0.3 in binary floating point.
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_large_numbers(self):
        self.assertAlmostEqual(add(1e15, 1e15), 2e15)


class TestSub(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertAlmostEqual(sub(5.5, 2.25), 3.25)

    def test_negative_result(self):
        self.assertAlmostEqual(sub(1.5, 4.0), -2.5)

    def test_negative_numbers(self):
        self.assertAlmostEqual(sub(-1.5, -2.5), 1.0)

    def test_zero(self):
        self.assertEqual(sub(0.0, 0.0), 0.0)
        self.assertAlmostEqual(sub(7.25, 0.0), 7.25)
        self.assertAlmostEqual(sub(7.25, 7.25), 0.0)

    def test_floating_point_rounding(self):
        # 0.3 - 0.1 is not exactly 0.2 in binary floating point.
        self.assertAlmostEqual(sub(0.3, 0.1), 0.2)


if __name__ == "__main__":
    unittest.main()
