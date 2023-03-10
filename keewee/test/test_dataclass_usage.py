import unittest
from dataclasses import dataclass, field

from keewee import KeeWee


@dataclass
class PokemonTrainer:
    name: str
    skill_level: int = field(default=KeeWee(), repr=False)


class MyTestCase(unittest.TestCase):

    def test_something(self):
        andrew = PokemonTrainer(name="Andrea Taylor", skill_level=0)
        self.assertEqual(andrew.skill_level, 0)
        andrew.skill_level = 1
        self.assertEqual(andrew.skill_level, 1)

        KeeWee.dump(file_name="andrea.json")

    def test_for_readme(self):
        import random
        from pprint import pprint

        ash = PokemonTrainer(name="Ash Ketchum", skill_level=0)

        for _ in range(10):
            ash.skill_level = random.randint(1, 10)
        pprint(
            KeeWee.dumpd()
        )


if __name__ == '__main__':
    unittest.main()
