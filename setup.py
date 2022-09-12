from setuptools import setup, find_packages


with open("README.md", "r") as doc:
    long_description = doc.read()

requirements = open("requirements.txt").read().split('\n')


setup(
    # General info
    name = 'tgstat_scraper',
    version = '0.0.1',
    description = 'TGSTAT website scraper',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/exorcistas/tgstat_scraper",
    author = "exorcistas",
    author_email = "exorcistas@github.com",

    # Packaging info
    packages=find_packages(),
    install_requires = [requirements],
)