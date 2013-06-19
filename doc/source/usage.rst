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

High-level overview
===================

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
are:

.. image:: _static/overview.png
   :align: center
