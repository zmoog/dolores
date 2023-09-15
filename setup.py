from setuptools import setup
import os

VERSION = "0.0.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="dolores",
    description="Discord bot",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Maurizio Branca",
    url="https://github.com/zmoog/dolores",
    project_urls={
        "Issues": "https://github.com/zmoog/dolores/issues",
        "CI": "https://github.com/zmoog/dolores/actions",
        "Changelog": "https://github.com/zmoog/dolores/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["dolores"],
    entry_points="""
        [console_scripts]
        dolores=dolores.cli:cli
    """,
    install_requires=[
        "click",
        "pydantic",
        "python-dotenv",
        "httpx",
        "rich",
        ],
    extras_require={
        "test": [
            "pytest",
            "pytest-recording",
            ]
    },
    python_requires=">=3.8",
)