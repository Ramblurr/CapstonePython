Capstone Python Demo
===================

Setup
-----

Follow the following instructions:

1. Check out source code
2. Create a virtual Python environment for dependencies
3. Install dependencies
4. Download dataset

Check out source code
---------------------

    git clone git://github.com/Ramblurr/CapstonePython.git

Create a virtual Python environment
-----------------------------------

This provides a simple and effective way to manage python
dependencies across platforms.

Install virtualenv:
If you are on linux you can install it via your package manager:
on Ubuntu/Debian:

    aptitude install python-virtualenv

on OpenSuse:

    zypper install python-virtualenv

otherwise install it with easy_install:

    easy_install -U virtualenv
    easy_install -U pip

Now let's create a new virtual environment, and begin using it:

    virtualenv capstone
    source capstone/bin/activate

Install dependencies
--------------------
Now let's install all of the dependencies:

    pip install -U -r requirements.txt

