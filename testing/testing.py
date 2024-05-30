import unittest

def add_numbers(a, b):
    return a + b

class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)

    def test_mixed_numbers(self):
        self.assertEqual(add_numbers(2, -3), -1)

if __name__ == '__main__':
    unittest.main()