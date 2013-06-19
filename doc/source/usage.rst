.. _usage:

*************
Using Uptrack
*************

The first time you run Uptrack, the home page may disappoint you.

Indeed, this is what you will see:

.. figure:: _static/overview-empty.png
   :align: center

   Uptrack's empty home page

You'll need to log in and start managing the application before it gets really
interesting.

But don't worry, the rest of this documentation will help you do just that.

.. _concepts:

General concepts
================

There are three fundamental concepts in Uptrack: **distributions**,
**upstreams** and **packages**.

Let's take an example to illustrate these...

Say you run *Foo Linux*, a community project to provide a free rebuild of a
well-known, but pricy, *Enterprise Linux*.

Your community has released 2 versions already, *Foo Linux 1* and
*Foo Linux 2*, and you are working on the thrid one, called *Foo Linux Next*
until the official release.

Each of your distributions, or "distro", is based on the corresponding
upstream versions: *Foo Linux 1* is based on *Enterprise Linux 1*, etc.

In addition, you add more packages to each version of *Foo Linux*, coming from
the corresponding *Entreprise Linux Extras* repository.

So, in Uptrack, the **distribution** called *Foo Linux 1* will have 2
**upstreams**: *Enterprise Linux 1* and *Enterprise Linux Extras 1*. Ditto for
your other distributions.

Now, for each **package** in a given **distribution**, Uptrack will compare
the latest version you have published with its last version in the appropriate
**upstream**.

And that is how it generates an overview of how up to date your distributions
are.

The overview
============

.. image:: _static/overview.png
   :align: center

Above is a screenshot of the main page of Uptrack, called the **overview**.

It lets you see at a quick glance how up to date the packages in your
distributions are, compared to their respective upstreams.

In the example above, one can see 3 "sections", one for each distribution. But
let's examine one more closely.

The table of freshness
----------------------

The first thing we see is a table.

On each line is an upstream, from which we take packages. Say we are looking
at the section of the overview related to *Foo Linux 1* in the above example.
As we can see, this distribution has packages coming from 2 upstreams:
*Enterprise Linux 1* and *Enterprise Linux Extras 1*.

Each line has 2 columns. The first displays the number of packages from that
upstream which are up to date in our distribution, while the second is for the
packages from that upstream which are out of date in our distribution.

For example, 21 packages coming from *Enterprise Linux 1* are out of date in
*Foo Linux 1*. Seems like the packager need to make a few builds to catch up
then!

Problematic packages
--------------------

Under the table is a line for the number of packages in this distribution
which Uptrack considered "problematic".

These can be in a number of situation:

1. Uptrack could not determine the upstream for the package
2. Uptrack could not find the upstream version for the package
3. The version of the package you published is newer than the upstream version
4. It's a bug, please :ref:`report it <report-bugs>` :-)

In some of the above cases, it could be that there is in fact no problem. For
example, it could be that you made a conscious decision to upgrade a package
before the new version was released by your upstream (case 3 above).

Uptrack has no way of knowing though, and as a result it will keep reminding
you that this package is not in a "normal" situation (i.e coming from a known
upstream package).

Details
-------

Did you observe that each number presented on the overview is clickable?

They will take you to the list of corresponding packages.

For example, in the above example, you could view the list of out of date
packages coming from *Enterprise Linux 2* in *Foo Linux 2* by clicking on the
number **40**.

And then get to work, those 40 packages won't become up to date on their own!

The default admin user
======================

By default the initialization script has created an administrator user, to let
you log in and manage the application.

* Login: ``admin``
* Password: ``admin``

It is probably a good idea to :ref:`create new admin users <manage-users>`
immediately, and delete this default account.

.. _manage-users:

Managing administrators
=======================

.. note:: Write this.
