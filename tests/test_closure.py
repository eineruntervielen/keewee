import unittest
import random

from src.keewee import keewee


class MyTestCase(unittest.TestCase):
    def test_something(self):
        x, set_x = keewee("x")
        for _ in range(10):
            set_x(random.randint(1, 10))
        print(x())


if __name__ == '__main__':
    unittest.main()
