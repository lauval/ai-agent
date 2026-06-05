# calculator/tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("3 + 5"), 8)

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("3 * 4"), 12)

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("10 / 2"), 5)

    def test_exponentiation(self):
        self.assertEqual(self.calculator.evaluate("2 ^ 3"), 8)
        self.assertEqual(self.calculator.evaluate("5 ^ 2"), 25)

    def test_modulo(self):
        self.assertEqual(self.calculator.evaluate("10 % 3"), 1)
        self.assertEqual(self.calculator.evaluate("5 % 2"), 1)

    def test_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "not allowed"):
            self.calculator.evaluate("10 / 0")

    def test_nested_expression(self):
        self.assertEqual(self.calculator.evaluate("3 * 4 + 5"), 17)

    def test_complex_expression(self):
        self.assertEqual(self.calculator.evaluate("2 * 3 - 8 / 2 + 5"), 7)

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(3 + 5) * 2"), 16)
        self.assertEqual(self.calculator.evaluate("10 / (2 + 3)"), 2)
        self.assertEqual(self.calculator.evaluate("10 / 2 + 3"), 8)

    def test_mismatched_parentheses(self):
        with self.assertRaisesRegex(ValueError, "Mismatched parentheses"):
            self.calculator.evaluate("(3 + 5 * 2")
        with self.assertRaisesRegex(ValueError, "Mismatched parentheses"):
            self.calculator.evaluate("3 + 5) * 2")

    def test_empty_expression(self):
        self.assertIsNone(self.calculator.evaluate(""))
        self.assertIsNone(self.calculator.evaluate("   "))

    def test_invalid_token(self):
        with self.assertRaisesRegex(ValueError, "Invalid token"):
            self.calculator.evaluate("3 + a")

    def test_invalid_expression(self):
        with self.assertRaisesRegex(
            ValueError, "Not enough operands for operator: \+"
        ):
            self.calculator.evaluate("3 +")
        with self.assertRaisesRegex(ValueError, "Invalid expression"):
            self.calculator.evaluate("3 5")

    def test_not_enough_operands(self):
        with self.assertRaisesRegex(ValueError, "Not enough operands for operator: \+"):
            self.calculator.evaluate("3 * 5 +")

    def test_float_numbers(self):
        self.assertAlmostEqual(self.calculator.evaluate("3.5 + 2.1"), 5.6)
        self.assertAlmostEqual(self.calculator.evaluate("10.5 / 2.5"), 4.2)

    def test_negative_numbers(self):
        self.assertEqual(self.calculator.evaluate("-3 + 5"), 2)
        self.assertEqual(self.calculator.evaluate("10 - -4"), 14)
        self.assertEqual(self.calculator.evaluate("-3 * -4"), 12)


if __name__ == "__main__":
    unittest.main()
