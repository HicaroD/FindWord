from setuptools import setup, find_packages

long_description = None
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="findwords",
    description="A simple CLI for finding the meaning of a word.",
    version="1.0.0",
    long_description=long_description,
    author="Hícaro",
    url="https://github.com/HicaroD/tChat",
    packages=find_packages("findword/"),
    install_requires=["requests", "termcolor"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts": [
            "findword = findword.main:_main",
        ]
    },
    python_requires=">=3.10"
)
