from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cz_oca",
    version="1.0.0",
    py_modules=["cz_oca"],
    author="Enric Tobella, Odoo Community Association (OCA)",
    author_email="f.krause@apheris.com",
    license="MIT",
    url="https://github.com/OCA/vz-oca",
    install_requires=["commitizen"],
    description="Extend the commitizen tools for OCA.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
