##############################
  Manage GitHub Repositories
##############################

A simple utililty to keep GitHub repositories syncronized.

.. note::

  It is assumed GitHub is used but any git repos is expected to work as long as you can access it (permissions).

I use macOS and Linux daily.  
I have created some aliases to support the script.
There is a ``Makefile`` to handle setting up, building and running the application.

If you are a Windows user then...

.. warning::

  | As always you should not trust content on the internet unconditionally.
  | Use at your own risk!

**********************
  Overview / Install
**********************

Requirements
============

The one actual requirement is ``GitPython``;
the rest are for convenience and cosmetics like colors and progress bars.
I like a progress bar but it does mean some of the methods updates a bar as a sideeffect.

.. image:: ./media/make_run_progress.png
  :width: 800

Feel free to omit the progress bar by modifying the script if you like - 
for example to be used by another script. 

The ``Makefile`` depends on the presence of ``make``.
You can get it by installing the Xcode command line tools.

Open a terminal and write:

.. code:: bash
  
  xcode-select --install

Accept the terms to install.

Optionally verify:

.. code:: bash

  xcode-select -p

You can see all the installed tools at: ``/Library/Developer/CommandLineTools/usr/bin``.

If you for example use ``git`` and it is not installed you will be asked to install,
which will do what the install command above does.

The CLI tools will update together with the regular OS updates and core applications like Safari.

You can choose the use Homebrew if you want the latest versions or don't want the Apple adapted/modified versions.

How to run
==========

macOS /Linux
------------

The following is added to my ``.zshenv`` file:

.. code:: bash
  
  export REPOS="~/source/repos"
  alias repos="cd $REPOS"
  alias grepos="cd $REPOS/GitHub"
  alias gsync="grepos;cd manage_github_repos;make run"

So I write ``gsync`` in a terminal.

.. image:: ./media/repo_list_all.png
  :width: 800

The meaning of colors... TODO

Oh-my-posh
----------

.. image:: ./media/prompt_dirty_repo.png
  :width: 580

A repository that is syncronized wih the remote will look like this:

.. image:: ./media/prompt_clean_repo.png
  :width: 580

.. image:: ./media/prompt_behind_repo.png
  :width: 580


