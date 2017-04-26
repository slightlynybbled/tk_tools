#!/usr/bin/env python

from setuptools import setup, find_packages


exec(open('tk_tools/version.py').read())

requirements = []

setup(name='tk_tools',
      version=__version__,
      description='Tkinter-native toolset',
      author='Jason R. Jones',
      author_email='slightlynybbled@gmail.com',
      url='',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False,
      )

