# KeeWee 🥝

Global application **state management** and **recording**.  
The Keewee library implements an auxiliary class that can be used to track values assigned to class and instance variables at runtime.  
One major usecase is to decouple your state-management from your business-logic
and keep your code nice and concise.  
You can also use it to record statistics about an attribute during runtime.  
The library works with regular `Python classes` or `dataclasses` but needs little different configuration.

## Installing

Install and update using [pip](https://pypi.org/project/keewee/)

````bash
$ pip install -U keewee
````

## A Simple Example

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
{
    'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": [0, 5, 9, 6, 3, 6, 10, 8, 4, 2, 9]}}
}
```

## Collection Record Modes

When assigning a KeeWee instance to an attribute,
the user can customize its internal recording-behavior by providing the `mode`-option.
Currently, there are four different modes, whereas the `list`-mode is the default setting.

### Direct mode

When only the current or resp. the last value is of interest, one can choose the `direct` mode,
where the attribute is _directely_ mapped
to its value.

````python
{
    'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": 3}}
}
````

### List mode

The `list`-mode keeps all occurring values in an ordered list from the first to the last value this attribute was assigned.  
Since this use-case is probably the _most_ common it is also chosen to be the *default* record-behavior.

```python
{
    'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": [0, 5, 9, 6, 3, 6, 10, 8, 4, 2, 9]}}
}
```

### Set mode

The `set`-modes only difference to the list-mode is that duplicates are not tracked.

```python
{
    'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": {0, 2, 3, 5, 7, 9}}}
}
```

### Datetime to value

If one wants to know exactly at what timestamp the modification took place the `dtv` (datetime-value)-mode is the best to choose.  
Here a new dictionary is created for every attribute and the current time is mapped onto the state change.

````python
{'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": {
    '15:11:44.976976': 0,
    '15:11:44.976985': 8,
    '15:11:44.976987': 6,
    '15:11:44.976990': 2,
    '15:11:44.976992': 6,
    '15:11:44.976994': 9,
    '15:11:44.976996': 8,
    '15:11:44.976998': 7,
    '15:11:44.977000': 3,
    '15:11:44.977002': 9,
    '15:11:44.977004': 7
}}}}
````

## Numerical Record Modes

The following record modes only work for numerical values, e.g.`int` or `float` etc.  
The result will look similar to the `direct`-mode.  
Currently there are three numerical record modes

1. `sum` the sum of all occurring values
2. `min` the minimal value that has occurred
3. `max` the maximum value that has occurred

An example usage for taking the _sum_ over all values could look like the following.

```python
@dataclass
class PokemonTrainer:
    name: str
    skill_level: int | KeeWee = field(default=KeeWee(mode='sum'), repr=False)
```

````python
{
    'PokemonTrainer': {'skill_level': {"PokemonTrainer(name='Ash Ketchum')": 49}}
}
````

## Links

- PyPI Releases: [https://pypi.org/project/keewee/](https://pypi.org/project/keewee/)