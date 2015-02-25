#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Ajax redirection wrapper/middleware for django
'''

from setuptools import setup, find_packages

LONG_DESC = str()

with open("README.md") as readme:
    LONG_DESC = readme.read()

setup(
    name="django-ajax-redirection",
    version="1.0.0",
    author="Hiroaki Yamamoto",
    author_email="admin@hysoftware.net",
    url="http://hysoftware.net",
    description="Useful wrappers/middleware for django",
    long_description=LONG_DESC,
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    zip_safe=False,
    install_requires=[
        "django"
    ],
    tests_requires=[
        "django",
        "nose",
        "flake8",
        "pylint"
    ]
)
