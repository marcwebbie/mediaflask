#!/usr/bin/env python

from setuptools import setup


__version__ = "0.2"

requirements = [pkg.strip() for pkg in open('requirements.txt').readlines()]

with open("README.rst") as f:
    long_description = f.read() + '\n'

setup(
    name='mediaflask',
    version=__version__,
    license='License :: OSI Approved :: MIT License',
    description="Download audio from online videos.",
    long_description=long_description,
    author='Marc Webbie',
    author_email='marcwebbie@gmail.com',
    url='https://github.com/marcwebbie/mediaflask',
    download_url='https://pypi.python.org/pypi/mediaflask',
    packages=['mediaflask'],
    install_requires=requirements,
    test_suite='tests.test',
    entry_points="""
        [console_scripts]
        mediaflask=mediaflask.web:main
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',
    ],
)
