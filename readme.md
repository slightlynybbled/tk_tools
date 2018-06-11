[![Build Status](https://travis-ci.org/slightlynybbled/tk_tools.svg?branch=master)](https://travis-ci.org/slightlynybbled/tk_tools)

[![Documentation Status](https://readthedocs.org/projects/tk-tools/badge/?version=latest)](http://tk-tools.readthedocs.io/en/latest/?badge=latest)

# Purpose

This repository holds useful high-level widgets written in pure python.  
This library used type hints and requires Python 3.5+; it could, however, be back-ported to earlier Python versions without difficulty.

For more details, check out the [documentation](https://tk-tools.readthedocs.io).

Here are some examples screenshots of the widgets you can create:

## Button-Grid:  

![Button-Grid](https://tk-tools.readthedocs.io/en/latest/_images/button-grid.png)

## Binary-Label:  

![Byte-Label](https://tk-tools.readthedocs.io/en/latest/_images/byte-label.png)

## Calendar:  

![Calendar](https://tk-tools.readthedocs.io/en/latest/_images/calendar.png)

## Dropdown:  

![Dropdown](https://tk-tools.readthedocs.io/en/latest/_images/dropdown.png)

## Entry-Grid:  

![Entry-Grid](https://tk-tools.readthedocs.io/en/latest/_images/entry-grid.png)

## Multi-Slot Frame

![Multi-Slot Frame](https://tk-tools.readthedocs.io/en/latest/_images/multi-slot-frame.png)

## Graph:  

![Graph](https://tk-tools.readthedocs.io/en/latest/_images/graph.png)

## Key-Value:  

![Key-Value](https://tk-tools.readthedocs.io/en/latest/_images/key-value.png)

## Label-Grid:  

![Label-Grid](https://tk-tools.readthedocs.io/en/latest/_images/label-grid.png)

## LED: (size can be scaled)  

![LED](https://tk-tools.readthedocs.io/en/latest/_images/led.gif)

## SevenSegment and SevenSegmentDisplay

![Seven Segment Display](https://tk-tools.readthedocs.io/en/latest/_images/seven-segment-display.png)

## Gauge

![Gauge](https://tk-tools.readthedocs.io/en/latest/_images/gauges.png)
![Gauge Documentation](https://tk-tools.readthedocs.io/en/latest/_images/gaugedoc.png)

## Rotary-Scale: (Tachometer)    

![Rotary-Scale](https://tk-tools.readthedocs.io/en/latest/_images/rotary-scale.png)

# Testing

Basic testing has been instantiated *however* it is currently limited.  To execute style testing:

    flake8 tk_tools
    
To execute automated tests:

    py.test test.py
    
More testing will be added to new widgets as they are brought online while further testing will be added to old widgets as the project matures.

# Contributions

Contributions for new widgets, documentation, tests, and resolving issues are welcomed.

Contribution guidelines:

1. Fork the repository to your account.
2. Clone your account repository to your local development environment.
3. Create/checkout a new branch appropriately named by feature, bug, issue number, whatever.
4. Make your changes on your branch. The ideal changes would:

 - have working examples in the examples directory
 - have documentation in the docs directory

5. Push your changes to your github account.
6. Create a pull request from within github.

All code is to be passing `flake8` before it is merged into master!
