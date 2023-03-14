import unittest

from src.keewee import keewee


class MyTestCase(unittest.TestCase):
    def test_something(self):
        get_x, set_x = keewee("x")
        set_x(5)
        self.assertEqual(get_x(), 5)


if __name__ == '__main__':
    unittest.main()
