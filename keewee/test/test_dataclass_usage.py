import unittest
from dataclasses import dataclass, field

from keewee import KeeWee


@dataclass
class PokemonTrainer:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(), repr=False)


class MyTestCase(unittest.TestCase):

    def test_something(self):
        def add_1(pokemon_trainer: PokemonTrainer) -> None:
            pokemon_trainer.skill_level += 1

        andrew = PokemonTrainer(name="Andrea Taylor", skill_level=0)
        self.assertEqual(andrew.skill_level, 0)
        andrew.skill_level = 1
        self.assertEqual(andrew.skill_level, 1)

        ash = PokemonTrainer(name="Ash Ketchum", skill_level=0)

        import random
        for _ in range(4):
            ash.skill_level = random.randint(1, 10)

        add_1(andrew)
        self.assertEqual(andrew.skill_level, 2)
        print(KeeWee.dump("test.json"))

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
