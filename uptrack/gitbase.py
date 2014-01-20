# Copyright (c) 2013 - Network Box
#
# This file is part of Uptrack.
#
# Uptrack is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Uptrack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Uptrack.  If not, see <http://www.gnu.org/licenses/>.


import multiprocessing
import os
import sys

import git


class subprocessed(object):
    """Decorator to run a function in a subprocess

    We can't use GitPython directly because it leaks memory and file
    descriptors:
        https://github.com/gitpython-developers/GitPython/issues/60

    Until it is fixed, we have to use multiple processes :(
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, *args, **kwargs):
        self.instance = instance
        return self

    def __call__(self, *args):
        from multiprocessing import Process, Queue
        q = Queue()

        def wrapper(queue, func, *args):
            queue.put(func(*args))

        p = Process(target=wrapper,
                    args=(q, self.func, self.instance) + args)
        p.start()
        p.join()

        if p.exitcode == 1:
            raise ValueError("Could not find the release branch: %s" % branch)

        if p.exitcode == 2:
            raise ValueError("Could not find an upstream branch")

        return q.get()


class GitBase(object):
    def __init__(self, git_clonedir, git_rooturl, upstream_prefix):
        self.git_clonedir = git_clonedir
        self.git_rooturl = git_rooturl
        self.upstream_prefix = upstream_prefix

        if not os.path.exists(self.git_clonedir):
            os.makedirs(self.git_clonedir)

    def __walk_for_upstream_branch(self, commit, ourbranch, up_prefix):
        """Find the upstream branch of a given commit

        This recursively walks through the history of a given commit, and
        tries to find the latest commit of a branch which was merged into
        it.

        :param commit: The git.Commit for which we walk the ancestry.
        :param ourbranch: The name of our branch, to make sure we don't
                          return it.
        :param up_prefix: The prefix representing upstream branches in our
                          naming convention.
        """
        parents = commit.parents
        if len(parents) == 0:
            # No parents, so no upstream branch
            return None

        # Check the parents quickly before checking each one's history, to
        # avoid wasting time on the history of the "wrong one" first.
        for parent in commit.parents:
            ref = parent.name_rev.split()[-1]

            if ref.startswith(ourbranch):
                # Still on our branch
                continue

            if "/" in ref:
                ref_parts = ref.split("/")

                if ref_parts[0] == "remotes" and \
                   ref_parts[2].startswith(up_prefix):
                    # We found it!
                    upstream = ref_parts[2]

                    if "~" in upstream:
                        upstream = upstream.split("~")[0]

                    return unicode(upstream)

        # Now for the long check down the history of each parent
        for parent in commit.parents:
            upstream = self.__walk_for_upstream_branch(parent, ourbranch,
                                                       up_prefix)
            if upstream:
                return upstream

        return None

    @subprocessed
    def get_upstream_branch(self, pkgname, branch_name):
        """Get the latest merged upstream branch

        :param pkgname: The name of the package in Git.
        :param branch_name: The name of the Git branch for the distro release.
        """
        curdir = os.getcwd()
        moduledir = os.path.join(self.git_clonedir, pkgname)

        if os.path.isdir(moduledir):
            repo = git.Repo(moduledir)
            repo.remotes.origin.fetch()

        else:
            repo = git.Repo.clone_from("%s/%s" % (self.git_rooturl, pkgname),
                                       moduledir)

        os.chdir(repo.working_tree_dir)

        try:
            repo.git.checkout(branch_name)
            repo.git.merge("origin/%s" % branch_name)
            branch = repo.head.reference

        except git.exc.GitCommandError:
            # We couldn't even find the release branch
            os.chdir(curdir)
            del repo

            sys.exit(1)

        up_branch = self.__walk_for_upstream_branch(branch.commit,
                                                    branch.name,
                                                    self.upstream_prefix)

        if not up_branch:
            # We couldn't find the upstream branch
            os.chdir(curdir)
            del repo

            sys.exit(2)

        # Clean up
        os.chdir(curdir)
        del repo

        return up_branch
