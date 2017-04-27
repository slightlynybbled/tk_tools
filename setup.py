#!/usr/bin/env python

from setuptools import setup, find_packages


exec(open('tk_tools/version.py').read())

requirements = []

setup(
    name='tk_tools',
    version=__version__,
    description='Tkinter-native toolset and widget library',
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/tk_tools',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English'
    ],
    keywords='tkinter gui widgets'
)

