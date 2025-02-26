# tests/test_utils.py

import unittest
from utils.temperature import get_temperature

class TestUtils(unittest.TestCase):
    def test_get_temperature(self):
        result = get_temperature("París")
        self.assertIn("°c", result.lower(), "La temperatura debe contener grados Celsius.")

if __name__ == "__main__":
    unittest.main()