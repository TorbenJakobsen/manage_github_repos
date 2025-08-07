.. _Homebrew: https://brew.sh/

##############################
  Manage GitHub Repositories
##############################

A simple utililty to keep GitHub repositories syncronized.

.. note::

  It is assumed GitHub is used but any git repository is expected to work
  as long as you can access it (permissions).

I use macOS and Linux daily.  
I have created some aliases to support the script.
There is a ``Makefile`` to handle setting up, building and running the application.

If you are a Windows user, the script also works and will described as well.

**********************
  Overview / Install
**********************

Requirements
============

The one actual requirement is ``GitPython``;
the rest of the Pysthon packages are for convenience and cosmetics like colors and progress bars.
I like a progress bar but it does mean some of the methods expects and updates a progress bar as a sideeffect.

.. image:: ./media/make_run_progress.png
  :width: 800

Feel free to omit the progress bar by modifying the script if you like - 
for example to be used by another script. 

The optional ``Makefile`` depends on the presence of ``make``.

The ``GitPython`` package uses an installed ``git`` thus ``git`` is also a dependency.

macOS
-----

You can get ``git`` and ``make`` by installing the Xcode command line tools.

Open a terminal and write:

.. code:: bash
  
  xcode-select --install

Accept the terms to install.

Optionally verify:

.. code:: bash

  xcode-select -p

You can see all the installed tools at: ``/Library/Developer/CommandLineTools/usr/bin``.

If you for example use ``git`` in macOS, and ``git`` is not installed,
you will be offered to install by the operating system,
which will do what the install command above does.

The Xcode CLI tools will update together with the regular OS updates and core applications like Safari.

You can choose the use Homebrew_ if you want the latest versions or don't want the Apple adapted/modified versions.

Windows
-------

...

Linux
-----


.. code:: bash

  # untested
  sudo apt install -y gcc git

How to run
==========

Configuration file
------------------

| The script needs a configuration file ``repos.csv``.
| In the project there is an ``example.csv`` file you can copy and modify.
| 

My preference is to make a symbolic link to a repository where my private/personal files are kept 
(no keys, tokens or account details).
As the script manages all repositories in the parent directory (from this repository)
one simply makes initial fetch so *this* repository and ``private-utils`` are present
before make the symbolic link.

.. code:: bash

  ln -sf ../private-utils/repos.csv ./repos.csv

If you make changes to the linked ``repos.csv`` make sure to push the change in ``private-utils/repos.csv``.

macOS /Linux
------------

The following is added to my ``.zshenv`` file:

.. code:: bash
  
  export REPOS="~/source/repos"
  alias repos="cd $REPOS"
  alias grepos="cd $REPOS/GitHub"
  alias gsync="grepos;cd manage_github_repos;make run"

So write ``gsync`` in a terminal. You will stay in the ``manage_github_repos`` directory.

.. image:: ./media/repo_list_all.png
  :width: 800

The meaning of colors... TODO

Oh-my-posh
----------

.. image:: ./media/prompt_dirty_repo.png
  :width: 580

A repository that is syncronized with the remote will look like this:

.. image:: ./media/prompt_clean_repo.png
  :width: 580

.. image:: ./media/prompt_behind_repo.png
  :width: 580


