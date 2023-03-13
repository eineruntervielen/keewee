import unittest
from dataclasses import dataclass


@dataclass
class Employee:
    id: str
    name: str
    position: str = "CEO"

    def __repr__(self):
        return f"<{self.id}|{self.name}>"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        first = Employee(id="1", name="bevor")
        print(first.position)
        namespace = {}
        exec("from dataclasses import dataclass, field", namespace)
        exec("from src.keewee import KeeWee", namespace)
        exec("@dataclass\n"
             "class Employee:\n"
             "    id: str\n"
             "    name: str = 'foo'\n"
             "    position: str = field(default=KeeWee(), repr=False)\n", namespace)
        x = namespace['Employee']
        print(x.position)
        namespace['KeeWee'].dump("test.json")


if __name__ == '__main__':
    unittest.main()
