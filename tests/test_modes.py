import unittest
from dataclasses import dataclass, field

from src.keewee import KeeWee


@dataclass
class PokemonTrainerSum:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(mode='sum'), repr=False)


@dataclass
class PokemonTrainerMax:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(mode='max'), repr=False)


@dataclass
class PokemonTrainerMin:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(mode='min'), repr=False)


class TestModes(unittest.TestCase):

    def test_mode_sum(self):
        pokemon_trainer = PokemonTrainerSum(name='Ash Ketchum', skill_level=0)
        pokemon_trainer.skill_level = 1
        self.assertEqual(KeeWee.dumpd().get("PokemonTrainerSum").get("skill_level").get("PokemonTrainerSum(name='Ash Ketchum')"), 1)

    def test_mode_max(self):
        pokemon_trainer = PokemonTrainerMax(name='Ash Ketchum', skill_level=0)
        pokemon_trainer.skill_level = 1
        self.assertEqual(KeeWee.dumpd().get("PokemonTrainerMax").get("skill_level").get("PokemonTrainerMax(name='Ash Ketchum')"), 1)
        pokemon_trainer.skill_level = 99
        self.assertEqual(KeeWee.dumpd().get("PokemonTrainerMax").get("skill_level").get("PokemonTrainerMax(name='Ash Ketchum')"), 99)

    def test_mode_min(self):
        pokemon_trainer = PokemonTrainerMin(name='Ash Ketchum', skill_level=0)
        pokemon_trainer.skill_level = 1
        self.assertEqual(KeeWee.dumpd().get("PokemonTrainerMin").get("skill_level").get("PokemonTrainerMin(name='Ash Ketchum')"), 0)
        pokemon_trainer.skill_level = -1
        self.assertEqual(KeeWee.dumpd().get("PokemonTrainerMin").get("skill_level").get("PokemonTrainerMin(name='Ash Ketchum')"), -1)


if __name__ == '__main__':
    unittest.main()
