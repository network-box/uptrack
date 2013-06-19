****************
Getting involved
****************

.. _contact:

Get in touch
============

At the moment, we don't have a mailing-list or a dedicated IRC channel, so for
now you can just
`send an email to Mathieu Bridon <mailto:bochecha[AT]fedoraproject[DOT]org>`_,
Uptrack's current main developer.

He can also be caught on IRC, under the nickname ``bochecha`` on Freenode.
However, because he lives in a UTC+8 timezone, you might not be awake at the
same time as he is.

.. _patches:

Send patches
============

Whether you want to fix a bug, add a new feature, or improve this
documentation, the procedure is the same.

1. Get the sources::

    $ git clone git://gitorious.org/bochecha-dayjob/uptrack.git
    $ cd uptrack

2. Make your changes, test them, and commit to your local Git repository.
3. Create your patch::

    $ git format-patch origin/master

4. :ref:`Send <contact>` us the patch!

For what is worth, we won't ask you to sign a copyright assignment or any
other long and tedious legal document, so keep them coming!

.. _report-bugs:

Report bugs
===========

Our bug tracker is with our mailing-list and IRC channel: they are nowhere to
be found. (well, Gitorious doesn't offer that feature yet)

So if you found a bug in Uptrack, the best right now is probably that you
:ref:`send an email <contact>` with all the details regarding the issue.

Or better yet, :ref:`send us a patch <patches>` to fix it!
