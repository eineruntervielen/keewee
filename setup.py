from setuptools import find_packages, setup

with open("README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="keewee",
    version="0.0.1",
    description="Useful descriptor for shadow stat collections",
    long_description=long_description,
    package_dir={"": "keewee"},
    packages=find_packages(where="keewee"),
    url="https://github.com/eineruntervielen/keewee",
    author="Erik J Kostic",
    license="GNU GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ]
)
