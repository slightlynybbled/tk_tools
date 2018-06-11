Installation
============

Pip
---

To install, simply ``pip install tk_tools``.  All images and other source material are included as packages within python, so you shouldn't have to do any funky workarounds even when using this package in pyinstaller or other static execution environments.  Some environments may require some basic modification to this, such as the use of `pip3` instead of `pip`.

Setup.py
--------

Clone the git repository, navigate to the cloned directory, and ``python3 setup.py install``.

Dependencies
------------

The tk_tools package is written with Python 3.5+ in mind! It uses type hints so that your IDE - such as PyCharm - can easily identify potential issues with your code as you write it. If you want this to support a different python version, create an issue and I'm sure that we can work something out easily enough.
