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
If you are on linux you can install it via your package manager.

on Ubuntu/Debian:

    aptitude install python-virtualenv

on OpenSuse:

    zypper install python-virtualenv

otherwise install it with easy_install:

    easy_install -U virtualenv
    easy_install -U pip

on windows you should be able to follow the above commands, but check this site
for  more info:

* http://wiki.pylonshq.com/display/pylonscookbook/Using+a+Virtualenv+Sandbox


Now let's create a new virtual environment, and begin using it:

    virtualenv capstone
    source capstone/bin/activate

Install dependencies
--------------------
Now let's install all of the dependencies:

    pip install -U -r requirements.txt

Download Dataset
---------------
Because the dataset(s) are huge and static they shouldn't be in source control.
So, you'll have to download them to your machine manually. git is set to ignore
them once they are downladed.

Download the dataset:

    cd data/
    ./download_data.sh

And you're done!

On windows, crack open the script and do what it does by hand.
