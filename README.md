# KeeWee

## Example:

Just define your Python classes or dataclasses as you would normally do.  
If you are using dataclasses you should remove your shadowing fields from
the `__repr__` as they will mess up your results in the end.

```python
from dataclasses import dataclass, field

from keewee import KeeWee


@dataclass
class PokemonTrainer:
    name: str
    skill_level: int = field(default=KeeWee(), repr=False)
```

A commong usage would look like

```python

import random

ash = PokemonTrainer(name="Ash Ketchum", skill_level=0)

for _ in range(10):
    ash.skill_level = random.randint(1, 10)

print(KeeWee.dumpd())
```

Result

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