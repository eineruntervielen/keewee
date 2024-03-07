import unittest

from keewee.keewee import KeeWee


class Employee:
    skill_level = KeeWee(mode="max")
    kids = KeeWee(mode="dtv")

    def __init__(self, name: str, skill_level: int):
        self.name = name
        self.skill_level = skill_level

    def __str__(self):
        return f"{self.name})"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        andrew = Employee(name="Andrea Taylor", skill_level=0)
        self.assertEqual(andrew.skill_level, 0)
        andrew.skill_level = 1
        andrew.skill_level = 1
        andrew.skill_level = 1
        andrew.skill_level = 3
        andrew.skill_level = 1
        self.assertEqual(andrew.skill_level, 1)

        andrew.kids = 1
        andrew.kids = 2
        KeeWee.pprint()


if __name__ == "__main__":
    unittest.main()
