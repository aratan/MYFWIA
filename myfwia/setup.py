# setup.py

from setuptools import setup, find_packages

setup(
    name="myfwia",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama",
        "duckduckgo-search"
    ],
)