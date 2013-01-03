import os

from setuptools import setup, find_packages

version = "0.55"

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'lxml',
    'python-dateutil'
    ]

setup(
    name = "trailer",
    packages = find_packages(),
    version = "{version}".format(version=version),
    description = "A model and parsers for GPX 1.0 and GPX 1,1 data.",
    long_description = README + '\n\n' +  CHANGES,
    author = "Robert Smallshire",
    author_email = "robert@smallshire.org.uk",
    url = "https://github.com/rob-smallshire/trailer/",
    download_url="https://github.com/rob-smallshire/trailer/archive/master.zip".format(version=version),
    keywords = ["Python"],
    license="MIT License",
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        ],
)
