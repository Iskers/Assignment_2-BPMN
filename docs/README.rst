.. Copyright 2020, Oskar T. Inderberg

==================================
Assignment 1: A New Control System
==================================

This program provides design, troubleshooting and analysis of projects

Getting Started
===============
This Python program requires at least python 3.5.

Features
--------
* Project design with the following parts:
    * Lanes containing gates and tasks
    * Gates
    * Tasks

* Simulate project duration and generate probability of completion within the given time frame
* Regression simulation using multiple models
* HTML generation with probabilities and model accuracies.
* Validate project validity
* Tested code with high coverage

Assumptions
------------
* Project following the correct pattern using lanes as containers for tasks
* Gates in which to reference for simulations
* Correctly initiated constraints for all nodes

Usage
-----
This project comes with a *main.py* file which is the base for running the deployed system. From here one can set
parameters as one want. For analysis of existing circuits import files into the data folder and load them.

.. code:: bash

    $ python main.py


Pumping Circuits
================
This program tries to conform to the practices used in the previous assignment and keep to them in a strict fashion.
Therefor a lot of the conventions used in this project will not be repeated in this README. These can be found in
Assignment 1.

File specifics
---------------

main.py
~~~~~~~
This is the file to be run by regular users for analysing circuits. It is run by using the function
``default_project_study()``. This can be edited to the users suited purpose.

The main way to customize projects is changing the source file so it represents the project you need analyzed.

Here one can edit the page_generator to simulate over the gate that one needs to simulate. One can also edit the
simulation count depending on how many trials one wishes. As the standard attributes of a project such as median,
averages durations are low computational costed they are done 10 times as many times. Dates is the last variable of
page generator and contains the time limit the user has for a project. This can be edited just above the page generator.


elements.py
~~~~~~~~~~~
This module contains all elements needed for creating a project as well as the project structure itself.
All classes are based on their designated abstractions as well as the top level ``ProjectElement`` class.

``Node`` is an abstraction for both Gate and Task giving them ability to share many of the same traits. One of these is
the member function factory which functions as a overall factory method for all node types. If one needed more node
types one can adjust this factory away from the if else pattern giving the ability to create a lot more types.
While the assignment recommended initiating nodes with a shared list of predecessors and successors an attempt was made
to have all nodes be independent of each other and only to be accessed in a context such as lane or project. While this
was done, it made some of the later processing hard had proved to be a time costly attempt.

``Container`` is an abstraction for project and lane and shares some traits with node. A change to optimize this would
be to add these shared traits and functions to the ``ProjectElement`` class. Examples of these are ``name`` and
``factory``, however one can make the argument that as they are not supposed to be accessed on this abstract level they
should be defined on the least abstract level and where they share the same use cases.
Container contains the property ``precedence_constraints`` which holds the constraints set for the project.

``PrecedenceConstraintsContainer`` is a class used in containers and is itself a container for the project constraints.
This class functions as a dictionary for all the nodes, and can be accessed in this way. If a user has a node and
it can be used to access the constraints coupled with it.

.. code:: python

    list_of_direct_predesessors = project.precedence_constraints[node]["From"]
    list_of_direct_successors = project.precedence_constraints[node]["To"]

One reminder is that this only gives back constraints in certain contexts. Some contexts do not contain next and
previous nodes because these constraints are defined in an project or lane context. This decision also proved to make
later processing more cumbersome and difficult.

simulation_tools.py
~~~~~~~~~~~~~~~~~~~

This file contains many generators which are used to generate different simulation results. ``DurationGenerators`` is
the used for ground level random number generation used to generate workloads for lanes and task durations.

``DateGenerator`` is used to generate dates for tasks and gates. These can be retrieved in order to find instance
project due date and gate due dates. It also contains a function ``project_reset`` which resets a project back to an
uninstanced original state where ``start_date`` and ``completion_dates`` for all project nodes are set back to -1.

``MonteCarloSimulation`` is used for top level project simulation and contains the class function ``Monte_Carlo_Basic``
which is its sole public function used outside of the file scope. It is used to generate results for the first part of
the HTML page where durations of the project provided are the base data that need to be processed.
This is also the function that generates the histogram.

``LabelStudy`` generates the labels used in assessing the performance of the chosen algorithms. It compares two lists
of labels and returns a description of their successes.

``AlgorithmStudy`` is the base for assessing the performance of the machine learning algorithms. Its functions takes in
a project, a gate name, a time limit and the amount of times to run the monte carlo simulation. It returns the results
in the form set in ``LabelStudy``.

page_generator.py
~~~~~~~~~~~~~~~~~
This file is used for generating HTML reports for projects. It holds two classes, ``HTMLSerializer`` and
``HTMLPageGenerator``. The first holds functions required for the latter. The latter is used in by main to generate a
HTML study file which represents the circuit. It has two public functions which can be used, either with custom circuits
or with the default circuit, which is *circuit.tsv* in *templates*. To simplify all HTML files and sources are in the
same folder: *templates*.

checker.py
~~~~~~~~~~

This file contains the ``Checker`` class which can be used to check whether or not a project is viable. Its member
function ``check_project`` takes in a projects and assesses whether it contains more than one start and one end gate.


src.printer.py
~~~~~~~~~~~~~~

Parser and printer works in much the same way. They take in some paths and either creates a project instance in the
program or outputs

circuit_control.py
~~~~~~~~~~~~~~~~~~
This file contains the ``CircuitControl`` class which is used to control circuits for faults. It is used by initializing
a class instance and then called with the function ``control_circuit`` which takes in a circuit and raises an exception
if a rule is broken. If no rule is broken it returns ``True``.

circuit_calculator.py
~~~~~~~~~~~~~~~~~~~~~
This file holds two classes. The first ``CircuitFormulas`` contains all the formulas used for the different calculations
used on a circuit. The second ``CircuitCalculator`` is the class used for retrieving the different calculations.
Modularizing the functions in such a way makes it easy to alter functions if needed and the calculator class remains
readable. One might want to change the function names in ``CircuitFormulas`` to make it more simple and flat.

The class ``CircuitFormulas`` contains a warning if the reynolds number exceeds 10^5. Remove the first if statement in
``calculate_flow_coefficient()`` to remove the warning.

study\_.py
~~~~~~~~~~
This file holds the class ``Study`` which, after initialized, can be called with a study function. This class takes
one argument and has one property, velocity. A study function
utilizes the classes private functions to perform some studies on a circuit. A circuit should be designed and controlled
before using these functions. If one is to create new studies they should be created as public member functions to be
called from this class.



Testing
-------

As testing and quality control of existing code is a important part of managing code, this program is developed with
the standard package unittest for testing. This gives the developer to easily and continuously test all parts of the
code concurrently with development.

To use this feature one has to:

.. code:: bash

    $ cd /path/to/project-dir/
    $ python -m unittest

Testing during this projects development is done using, as mentioned earlier, the packages **unittest** as well as
**coverage**. Coverages gives the developer an overview of what lines of code has been run. The tests developed have
tried to provide 100% line coverage to ensure that all lines have been tested and gives the expected response.

Testing has also been done with coverage, and a report has been generated showing what lines have been tested and which
have not been tested with the current method. All necessary tests have been run, but are not included in tests.

Modularisation
--------------

As this python program is composed of several modules and data sets it is departmentalized into different folders.
Reviewing the project structure, it is composed of the folders data, tests and module, as well as a top facing
main function. Basing the project such provides a clear overview and modularize's the project into easy accessible
files without overwhelming the user.

This is an attempt to create files which can be copied and pasted to new projects when needed. For example
*file_handler.py* and *parser.py* are meant to be easily adapted for new projects. Furthermore modularizing classes
which dont share inheritance seemed like a useful standard.

.. Compared to many other projects this project is modularized in quite a degree.

Documentation, docstrings and annotations
------------------------------------------

In an attempt to develop this project in a more realistic manner, close to a real world open-source project I have
tried to use the conventions of creating a README and use `docstrings <https://www.python.org/dev/peps/pep-0257/>`_
and `annotations <https://www.python.org/dev/peps/pep-3107/>`_.

These have been used to give new developers an idea of what a function takes in and outputs. Using with an IDE which
supports docstrings helps developers in a great deal when sorting through use of the code.

Discovering these conventions during development has led to some inconsistencies in the project.



Afterthoughts
~~~~~~~~~~~~~
I should have decided on some conventions in the start of the project and kept to them. Refactoring and changing
conventions midway was very time consuming and with led to a lot of issues.

Consistency is key. When working on big projects, if one does not keep to decided standards it makes it hard to alter
code after not using it for some time. In my case after reading about properties and factory functions, it may have
saved me a lot of time not to adapt them until the next project.


:Author:
    Oskar T. Inderberg
:Version:
    1.0
:Date created: 03.02.2020
:Last updated: 08.03.2020