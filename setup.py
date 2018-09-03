#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['begins', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Jeremie Pardou",
    author_email='jpardou@makina-corpus.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Smart file import with auto type detection.",
    entry_points={
        'console_scripts': [
            'smartimport=smartimport.cli:main.start',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='smartimport',
    name='smartimport',
    packages=find_packages(include=['smartimport']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    #url='https://github.com/jrmi/smartimport',
    version='0.1',
    zip_safe=False,
)
