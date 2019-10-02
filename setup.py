from setuptools import setup

version = "0.1.0"

with open("./README.md") as fd:
    long_description = fd.read()

setup(
    name="path2json",
    version=version,
    description=
    "Convert whatever is the end of a directory path to JSON",
    long_description=long_description,
    install_requires=[
    ],
    author="Lee Kamentsky",
    packages=["path2json"],
    entry_points={ 'console_scripts': [
        "path2json=path2json.main:main"
    ]},
    url="https://github.com/LeeKamentsky/path2json",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.5'
    ]
)