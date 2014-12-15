PaPI v. 0.7
==================

Plugin based Process Interaction

Introduction
------
PaPI is a tool to interact with data generating processes. It can be used to get data stream of experiments or devices
like oscilloscopes.

PaPI is based on a strong plugin architecture. Therefore it is easy to expand to new environments.

PaPi will make heavily use of multi-core systems.

Installation
------
Basic installation on Ubuntu 14.04 64Bit

`sudo apt-get install git python3-pyside python3-numpy python3-scipy`

`git clone https://github.com/TUB-Control/PaPI.git PaPI`

`cd PaPI`

`python3 main.py`


Documentation
------

Sphinx doc on GitHub: https://tub-control.github.io/PaPI/

PaPI wiki on GitHub: https://github.com/TUB-Control/PaPI/wiki


Changelog
------

v.0.8
---

* Use plugin as wizards for configurations
* Use ESC and RETURN for window interaction
* New file dialog to avoid performance issues
* [fix] signal names instead of id in overview
* Run/Edit mode
* Set/load backgorund and save it to config
* [fix] When plugin in gui crashs, gui stays alive and plugin will be stopped