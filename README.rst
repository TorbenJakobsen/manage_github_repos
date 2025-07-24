##############################
  Manage GitHub Repositories
##############################

A simple utililty to keep GitHub repositories syncronized.

I use macOS and Linux daily.  
I have created some aliases to support the script.
There is a ``Makefile`` to handle setting up, building and run the application.

If you are a Windows user then...

.. warning::
  As always you should not trust content on the internaet uncondiationally.
  Use at your own risk!

**********************
  Overview / Install
**********************

Requirements
============

The one central requirement is ``GitPython``;
the rest are for convenience and cosmetics like colors and progress bars.
I like a progres bar but it means some of the methods updates a bar as a side effect.

.. image:: ./media/make_run_progress.png
  :width: 620

Feel free to omit the progress bar by midifying the script if you like - 
for example to be used by other scripts. 

The ``Makefile`` depends on the presence of ``make``.
You can get it by installing the Xcode command line tools.

Open a terminal and write:

.. code:: bash
  xcode-select --install

Accept the terms to install.

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

Oh-my-posh
----------

.. image:: ./media/prompt_dirty_repo.png
