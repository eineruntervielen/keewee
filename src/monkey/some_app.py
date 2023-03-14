import random
import logging

from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)


@dataclass
class Worker:
    name: str
    w_id: str
    skill_lvl: int


def business_logic(worker: Worker):
    for _ in range(10):
        worker.skill_lvl = random.randint(1, 10)


def main():
    logging.info(msg="  +-----------------------------------------------------+")
    logging.info(msg="  Initialize first worker")
    #
    worker = Worker(name="Worker1", w_id="1", skill_lvl=0)
    #
    logging.info(msg=f"    {worker}")
    logging.info(msg="  Calling business logic from within main function")
    #
    business_logic(worker)
    #
    logging.info(msg="  Business logic has ended in main function")
    logging.info(msg=f"    {worker}")
    logging.info(msg="  +-----------------------------------------------------+")


if __name__ == "__main__":
    main()
