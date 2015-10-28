Git useful commands
===================

http://rogerdudler.github.io/git-guide/index.it.html  
http://www.brunosanteramo.com/en/2015/10/22/git-useful-commands/

List tags
---------
::

    git tag

Create tag
----------

command:
::

    git tag <tag_name> <commit_id>

example:
::

    git tag 0.1 1b2e1d63ff

commit id be retrieved via:
::

    git log

Push tags
---------

Push all tags:
::

    git push --tags

Push a single tag:
::

    git push origin <tag_name>

List branch
-----------
::

    git branch

Create new branch and switch to new branch
------------------------------------------
::

    git checkout -b <branch_name>

Switch branch
-------------
::

    git checkout <branch_name>

Remove branch
-------------
::

    git branch -d <branch_name>

Push changes to branch
----------------------
::

    git push origin <branch_name>
