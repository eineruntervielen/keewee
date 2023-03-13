import unittest

from src.keewee import KeeWee


class Employee:
    name = KeeWee()
    skill_level = KeeWee()

    def __init__(self, name: str, skill_level: int):
        self.name = name
        self.skill_level = skill_level

    def __str__(self):
        return f"Employee( name: {self.name})"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        andrew = Employee(name="Andrea Taylor", skill_level=0)
        self.assertEqual(andrew.skill_level, 0)
        andrew.skill_level = 1
        self.assertEqual(andrew.skill_level, 1)

        # KeeWee.dumpd()
        KeeWee.dump(file_name="andrea.json")


if __name__ == "__main__":
    unittest.main()
