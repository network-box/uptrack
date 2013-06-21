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

.. _code:

Contribute code
===============

We welcome bug fixes or improvements, both to the Uptrack code or its
documentation.

In addition, we won't ask you to sign a copyright assignment or any
other long and tedious legal document, so don't hesitate any second and send
us your changes!

We prefer merge requests, but we won't refuse plain old patches anyway. Pick
the method you prefer.

Open a merge request
--------------------

This is a bit more demanding on you at first than the next method, but it's
also much easier for everybody in the long run if you contribute regularly to
Uptrack. Which is why we prefer that method: we'd really like to have you as a
long-term contributor. :)

Here are the basic steps:

1. `Clone Uptrack on Gitorious`_.

2. Get the sources from both the central repo and your fork::

    $ git clone -o mine git@gitorious.org:<your fork>
    $ cd uptrack
    $ git remote add upstream git://gitorious.org/bochecha-dayjob/uptrack.git
    $ git fetch upstream

   Use your favourite log viewer to visualize how both remotes are currently
   synchronized.

3. Make your changes, test them, and commit them.

4. Use the Gitorious web interface to open the merge request.

.. _Clone Uptrack on Gitorious: https://gitorious.org/bochecha-dayjob/uptrack/clone


Send a patch
------------

This is the quickest method for drive-by contributions, no need to maintain a
public clone and keep merging/rebasing with the changes we make.

It goes like this:

1. Get the sources::

    $ git clone git://gitorious.org/bochecha-dayjob/uptrack.git
    $ cd uptrack

2. Make your changes, test them, and commit to your local Git repository.
3. Create your patch::

    $ git format-patch origin/master

4. :ref:`Send <contact>` us the patch!

.. _report-bugs:

Report bugs
===========

Our bug tracker is with our mailing-list and IRC channel: they are nowhere to
be found. (well, Gitorious doesn't offer that feature yet)

So if you found a bug in Uptrack, the best right now is probably that you
:ref:`send an email <contact>` with all the details regarding the issue.

Or better yet, :ref:`send us a fix <code>` to fix it!
