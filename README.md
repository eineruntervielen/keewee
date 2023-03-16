# KeeWee 🥝

Keewee is an auxiliary class that implements the descriptor-protocol.  
One major usecase is to record statistical data about an attribute of a class during runtime.  
The library works with regular `Python classes` or `dataclasses`.

## Installing

Install and update using [pip](https://pypi.org/project/keewee/)

````bash
$ pip install -U keewee
````

## A Simple Example (wordless)

````python
import random

from dataclasses import dataclass, field
from keewee import KeeWee


@dataclass
class PokemonTrainer:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(), repr=False)


if __name__ == "__main__":
    ash = PokemonTrainer(name="Ash Ketchum", skill_level=0)
    for _ in range(10):
        ash.skill_level = random.randint(1, 10)
    print(KeeWee.dumpd())
````

```python
{'PokemonTrainer':
    {'skill_level':
        {"PokemonTrainer(name='Ash Ketchum')": {
            '13:08:36.055042': 0,
            '13:08:36.055055': 5,
            '13:08:36.055059': 1,
            '13:08:36.055061': 5,
            '13:08:36.055064': 2,
            '13:08:36.055066': 5,
            '13:08:36.055069': 10,
            '13:08:36.055071': 6,
            '13:08:36.055073': 6,
            '13:08:36.055075': 6,
            '13:08:36.055077': 4
        }
        }
    }
}
```

## Record Modes

The different modes provide a convenient way of recording
the properties / variables states in a concise manner.
KeeWees default mode is set to `list` which seems to be a common use-case.  The 

| Mode | int | float | bool | str | list |
|------|-----|-------|------|-----|------|
| list | ✅   | ✅     | ✅    | ✅   | ❌    |
| set  | ✅   | ✅     | ✅    | ✅   | ❌    |
| dict | ✅   | ✅     | ✅    | ✅   | ❌    |

## A Bigger Example

...

## Links

- PyPI Releases: [https://pypi.org/project/keewee/](https://pypi.org/project/keewee/)