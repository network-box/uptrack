*****************
Deploying Uptrack
*****************

Because it is such a young project, we recommend you get the source code from
Git, and deploy it in a virtual environment.

Eventually, we'll have packages in various distributions which will make the
whole process easier, but this will come later.

Get the source code from Git
============================

Uptrack is hosted on Gitorious. Obtaining the source code is as easy as
running a simple command::

    $ git clone git://gitorious.org/bochecha-dayjob/uptrack.git

The rest of this page assumes that you are inside the root directory of the
source code, so you probably should get in there now::

    $ cd uptrack

Create a virtual environment
============================

Most dependencies for Uptrack are available on `Pypi`_... but unfortunately,
not all of them (for example the `yum`_ module).

As a result, you will need to let your virtual environment access the system
Python packages.

From the root directory of your Uptrack clone::

    $ virtualenv --system-site-packages venv

.. note:: The rest of this page assumes that your virtual environment is
   active.

Then, activate the virtual environment::

    $ . ./venv/bin/activate

Install the dependencies
========================

Uptrack requires the following Python modules as dependencies:

.. note:: The versions indicated here are the ones with which Uptrack has
   been tested. If you find it works with other versions, let us know!

* py-bcrypt
* colander
* deform
* deform_bootstrap
* koji             (1.7.0)
* pyramid
* pyramid_tm
* rpm              (4.8.0)
* sqlalchemy
* transaction
* yum              (3.2.29)
* zope.sqlalchemy

Some of them **must** be installed in your system Python installation, as they
do not exist on Pypi. On Enterprise Linux 6, you can run::

    # yum install koji rpm-python yum

Fortunately, the rest are all available in Pypi, so you should be able to get
them by running::

    $ python setup.py develop

This will setup the development source tree in your virtual environment, so
that the application can be run, while installing all the dependencies.

Deploy the application
======================

Before running it, there is one last step: initializing the database.

This is achieve through a simple script::

    $ uptrack-initdb development.ini

Your application is now ready to be run::

    $ pserve development.ini

Open your web browser, and take it to http://127.0.0.1:6543, then start
:ref:`using Uptrack <usage>`.

.. _Pypi: https://pypi.python.org/
.. _yum: http://yum.baseurl.org/
