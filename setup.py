from setuptools import setup

setup(
    name="django-nimbus",
    version="0.1",
    description="Reusable utilities for Django",
    long_description="Reusable utilities for Django projects, including handling files and sorting.",
    keywords="django, utilities",
    author="Josh Stegmaier <jrs@joshstegmaier.com>",
    author_email="jrs@joshstegmaier.com",
    url="https://github.com/JoshStegmaier/django-nimbus/",
    license="MIT",
    packages=["nimbus", "nimbus.filehandling", "nimbus.util", "nimbus.views"],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)