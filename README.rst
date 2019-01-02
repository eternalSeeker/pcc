=========================
 Python Project Template
=========================

.. image:: https://travis-ci.org/seanfisk/python-project-template.png
   :target: https://travis-ci.org/seanfisk/python-project-template

This project is intended to give an insight into the operation of a conmpiler. This compiler is written in Python and is optimized for readability of the source code rather than speed or size of the executables it produces.

Project Setup
=============

This will be the ``README`` for your project. For now, follow these instructions to get this project template set up correctly. Then, come back and replace the contents of this ``README`` with contents specific to your project.

Instructions
------------

#. Clone the template project, replacing ``my-project`` with the name of the project you are creating::

        git clone https://github.com/eternalSeeker/pcc.git my-project
        cd my-project

#. *(Optional, but good practice)* Create a new virtual environment for your project:

   With pyenv_ and pyenv-virtualenv_::

       pyenv virtualenv my-project
       pyenv local my-project

   With virtualenvwrapper_::

       mkvirtualenv my-project

   With plain virtualenv_::

       virtualenv /path/to/my-project-venv
       source /path/to/my-project-venv/bin/activate

   If you are new to virtual environments, please see the `Virtual Environment section`_ of Kenneth Reitz's Python Guide.

#. Install the project's development and runtime requirements::

        pip install -r requirements-dev.txt

#. Run the tests::

        paver test_all

   You should see output similar to this::

       $ paver test_all
       ---> pavement.test_all
       No style errors
       ============================================ test session starts =============================================
       platform cygwin -- Python 3.6.4, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
       rootdir: /cygdrive/c/Users/Bart/Downloads/pcc, inifile:

       collected X items

       tests/test_main.py .....
       <other tests>

       ====================================== X passed in Y.ZZ seconds =======================================
         ___  _   ___ ___ ___ ___
        | _ \/_\ / __/ __| __|   \
        |  _/ _ \\__ \__ \ _|| |) |
        |_|/_/ \_\___/___/___|___/

   The substitution performed is rather naive, so some style errors may be reported if the description or name cause lines to be too long. Correct these manually before moving to the next step. If any unit tests fail to pass, please report an issue.

**Project setup is now complete!**

.. _pyenv: https://github.com/yyuu/pyenv
.. _pyenv-virtualenv: https://github.com/yyuu/pyenv-virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/index.html
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _Virtual Environment section: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Using Paver
-----------

The ``pavement.py`` file comes with a number of tasks already set up for you. You can see a full list by typing ``paver help`` in the project root directory. The following are included::

    Tasks from pavement:
    lint                 - Perform PEP8 style check, run PyFlakes, and run McCabe complexity metrics on the code.
    doc_open             - Build the HTML docs and open them in a web browser.
    coverage             - Run tests and show test coverage report.
    doc_watch            - Watch for changes in the Sphinx documentation and rebuild when changed.
    test                 - Run the unit tests.
    get_tasks            - Get all paver-defined tasks.
    commit               - Commit only if all the tests pass.
    test_all             - Perform a style check and run all unit tests.
    generate_testOutputs - Generate the output for the self generated test inputs

For example, to run the both the unit tests and lint, run the following in the project root directory::

    paver test_all

To build the HTML documentation, then open it in a web browser::

    paver doc_open

Using Tox
---------

Tox is a tool for running your tests on all supported Python versions.
Running it via ``tox`` from the project root directory calls ``paver test_all`` behind the scenes for each Python version,
and does an additional test run to ensure documentation generation works flawlessly.
You can customize the list of supported and thus tested Python versions in the ``tox.ini`` file.

Pip ``requirements[-dev].txt`` files vs. Setuptools ``install_requires`` Keyword
------------------------------------------------------------------

The difference in use case between these two mechanisms can be very confusing. The `pip requirements files`_ is the conventionally-named ``requirements.txt`` that sits in the root directory of many repositories, including this one. The `Setuptools install_requires keyword`_ is the list of dependencies declared in ``setup.py`` that is automatically installed by ``pip`` or ``easy_install`` when a package is installed. They have similar but distinct purposes:

``install_requires`` keyword
    Install runtime dependencies for the package. This list is meant to *exclude* versions of dependent packages that do not work with this Python package. This is intended to be run automatically by ``pip`` or ``easy_install``.

pip requirements file
    Install runtime and/or development dependencies for the package. Replicate an environment by specifying exact versions of packages that are confirmed to work together. The goal is to `ensure repeatability`_ and provide developers with an identical development environment. This is intended to be run manually by the developer using ``pip install -r requirements-dev.txt``.

For more information, see the answer provided by Ian Bicking (author of pip) to `this StackOverflow question`_.

.. _Pip requirements files: http://www.pip-installer.org/en/latest/requirements.html
.. _Setuptools install_requires keyword: http://pythonhosted.org/setuptools/setuptools.html?highlight=install_requires#declaring-dependencies
.. _ensure repeatability: http://www.pip-installer.org/en/latest/cookbook.html#ensuring-repeatability
.. _this StackOverflow question: http://stackoverflow.com/questions/6947988/when-to-use-pip-requirements-file-versus-install-requires-in-setup-py


Licenses
========

.. _`Python Software Foundation License`: https://docs.python.org/3/license.html
.. _`Sphinx Simplified BSD License`: https://github.com/sphinx-doc/sphinx/blob/master/LICENSE
.. _`Paver Modified BSD License`: https://github.com/paver/paver/blob/master/LICENSE.txt
.. _`colorama Modified BSD License`: https://github.com/tartley/colorama/blob/master/LICENSE.txt
.. _`flake8 MIT/X11 License`: https://gitlab.com/pycqa/flake8/blob/master/LICENSE
.. _`mock Modified BSD License`: https://github.com/testing-cabal/mock/blob/master/LICENSE.txt
.. _`pytest MIT/X11 License`: https://docs.pytest.org/en/latest/license.html
.. _`tox MIT/X11 License`: https://github.com/tox-dev/tox/blob/master/LICENSE

The code which makes up this Python project template is licensed under the MIT/X11 license. Feel free to use it in your free software/open-source or proprietary projects.
The template also uses a number of other pieces of software, whose licenses are listed here for convenience. It is your responsibility to ensure that these licenses are up-to-date for the version of each tool you are using.

+------------------------+---------------------------------------+
|Project                 |License                                |
+========================+=======================================+
|Python itself           |`Python Software Foundation License`_  |
+------------------------+---------------------------------------+
|Sphinx                  |`Sphinx Simplified BSD License`_       |
+------------------------+---------------------------------------+
|Paver                   |`Paver Modified BSD License`_          |
+------------------------+---------------------------------------+
|colorama                |`colorama Modified BSD License`_       |
+------------------------+---------------------------------------+
|flake8                  |`flake8 MIT/X11 License`_              |
+------------------------+---------------------------------------+
|mock                    |`mock Modified BSD License`_           |
+------------------------+---------------------------------------+
|pytest                  |`pytest MIT/X11 License`_              |
+------------------------+---------------------------------------+
|tox                     |`tox MIT/X11 License`_                 |
+------------------------+---------------------------------------+

This project was based on the https://github.com/seanfisk/python-project-template/ from Sean Fisk and Benjamin Schwarze.

Issues
======

Please report any bugs or requests that you have using the GitHub issue tracker!

Development
===========

If you wish to contribute, first make your changes. Then run the following from the project root directory::

    source internal/test.sh

This will copy the template directory to a temporary directory, run the generation, then run tox. Any arguments passed will go directly to the tox command line, e.g.::

    source internal/test.sh -e py27

This command line would just test Python 2.7.

Authors
=======

* Bart Opsomer
