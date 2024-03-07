import json
import pprint
import importlib
import inspect
import logging

from dataclasses import dataclass, field

from src import KeeWee

logging.basicConfig(level=logging.DEBUG)


def run_from():
    with open("keewee.config.json", "r") as f:
        kw = json.load(f)
    testmain = importlib.import_module(kw["module"])
    print(testmain)
    print(testmain["Worker"])


def monkey_patch():
    import some_app
    DC_ATT_STR = "{}"
    DC_FIELD_STR = "dataclasses.field(default=KeeWee(), repr=False)"
    patch_str = "    skill_lvl: int | KeeWee = field(default=KeeWee(), repr=False)\n"
    source_worker, _ = inspect.getsourcelines(some_app.Worker)
    source_worker[4] = patch_str
    exec("".join(source_worker))
    some_app.Worker = locals()["Worker"]
    logging.info(msg="  ")
    some_app.main()
    logging.info(msg="  ")

    logging.info(msg=pprint.pformat(KeeWee.dumpd()))


if __name__ == "__main__":
    monkey_patch()
    # run_from()
