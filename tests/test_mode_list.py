import unittest

from dataclasses import dataclass, field
from pprint import pprint
from random import randint

from src.keewee import KeeWee


@dataclass
class Employee:
    id: str
    name: str
    position: str | KeeWee = field(default=KeeWee(mode="dtv"), repr=False)
    skill_lvl: int | KeeWee = field(default=KeeWee(mode="list"), repr=False)

    def __repr__(self):
        return f"<{self.id}|{self.name}>"


class TestModeList(unittest.TestCase):

    def setUp(self) -> None:
        self.e1 = Employee(id="1", name="First", position="CEO", skill_lvl=0)
        self.e2 = Employee(id="2", name="Second", position="STUDENT", skill_lvl=0)

    def test_something(self):
        self.e1.position = "COO"
        self.e1.position = "COO"
        self.e1.position = "COO"
        self.e1.position = "COO"
        self.e1.position = "COOL"
        self.e2.position = "WERKSTUDENT"
        for _ in range(5):
            self.e2.skill_lvl = randint(1, 10)
        KeeWee.pprint()


if __name__ == '__main__':
    unittest.main()
