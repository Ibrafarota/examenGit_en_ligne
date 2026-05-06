"""Tests unitaires pour mesfonctions.py."""

import unittest

from mesfonctions import (
    addition,
    compter_voyelles,
    division,
    est_premier,
    factorielle,
)


class TestMesFonctions(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(addition(2, 5), 7)

    def test_division(self):
        self.assertEqual(division(10, 2), 5)

    def test_factorielle(self):
        self.assertEqual(factorielle(5), 120)

    def test_est_premier(self):
        self.assertTrue(est_premier(13))
        self.assertFalse(est_premier(21))

    def test_compter_voyelles(self):
        self.assertEqual(compter_voyelles("Bonjour IA"), 5)


if __name__ == "__main__":
    unittest.main()
