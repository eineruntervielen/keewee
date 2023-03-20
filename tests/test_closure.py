import unittest

from src.keewee import keewee, KeeWee


class ClosureKeeWee(unittest.TestCase):
    def setUp(self) -> None:
        self.x, self.set_x = keewee(name="x", initial=1)

    def test_dunder_eq(self):
        self.assertEqual(self.x, 1)

    def test_dunder_repr(self):
        self.assertEqual(repr(self.x), "1")

    def test_mutating(self):
        self.set_x(5)
        self.assertEqual(self.x, 5)

        KeeWee.pprint()


if __name__ == '__main__':
    unittest.main()
