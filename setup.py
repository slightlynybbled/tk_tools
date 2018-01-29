#!/usr/bin/env python

from setuptools import setup
from stringify import stringify_py
import os

# provide correct path for version
__version__ = None
here = os.path.dirname(os.path.dirname(__file__))
exec(open(os.path.join(here, 'tk_tools/version.py')).read())

# archive the image files into 'tk_tools/images.py'
stringify_py('images', 'tk_tools/images.py')

requirements = [
    'xlrd >= 1.0.0',
    'xlwt >= 1.0.0'
]

setup_requirements = [
    'flake8 >= 3.5.0',
    'stringify >= 0.1.1',
    'sphinx >= 1.6'
]

setup(
    name='tk_tools',
    version=__version__,
    description='Tkinter-native toolset and widget library',
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/tk_tools',
    packages=['tk_tools'],
    include_package_data=True,
    install_requires=requirements,
    setup_requires=setup_requirements,
    zip_safe=True,
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
