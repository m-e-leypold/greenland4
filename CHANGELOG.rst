=========
Changelog
=========

.. note::
   
   All notable changes to this project will be documented in this file.

   The format is based on `Keep a Changelog`_ and this project adheres
   to `Semantic Versioning`_, as far as compatible with `PEP 440`_.

.. _Keep a Changelog:    https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
.. _PEP 440:              https://www.python.org/dev/peps/pep-0440/


Unreleased
==========


Release 0.0.5_
==============

URL: `https://github.com/m-e-leypold/greenland4/release/0.0.5 <0.0.5_>`_

.. _0.0.5: https://github.com/m-e-leypold/greenland4/releases/tag/release%2F0.0.5

- [NEW]: "Master" Regex (greenland.parsing.master_regex): Use a list of
  regular expression to match against a string, dependend on regular
  expression matching dispatch to constructor and return constructed
  item.
- Using a local temporary directory for test fixures now (--basetemp)
- Known Bugs: 190119a. 
- [NEW] fileystem.trees: Object model for filesystem traversal,
  methods for finding files.
- [NEW] fileystem.find: Finding files and directories, useful
  predicates on filesystem objects.
- More documentation in README.rst and about.rst. A simple example to
  showcase what Greenland can provide so far.
  
Release 0.0.4_
==============

URL: `https://github.com/m-e-leypold/greenland4/release/0.0.4 <0.0.4_>`_

.. _0.0.4: https://github.com/m-e-leypold/greenland4/releases/tag/release%2F0.0.4


- Incremented version, in order to supersede defective 0.0.2 release on PyPi.


Release 0.0.2_
==============

URL: `https://github.com/m-e-leypold/greenland4/release/0.0.2 <0.0.2_>`_

.. _0.0.2: https://github.com/m-e-leypold/greenland4/releases/tag/release%2F0.0.2


- Checking by flake8, disabled E501 (long lines), as well as E251,
  E221 (both related to aligning keyword arguments between lines). Not
  run per default yet.
- Added a change log: :code:`CHANGELOG.rst`.
- Marked install vs. development requirements in requirements.txt
- Fixed installation metadata in setup.py


Release 0.0.1_
==============

URL: `https://github.com/m-e-leypold/greenland4/release/0.0.1 <0.0.1_>`_

.. _0.0.1: https://github.com/m-e-leypold/greenland4/releases/tag/release%2F0.0.1


Added
-----

- Commandline parsers + prefab applications (:code:`greenland.cmdline`).
- Predicates for point-free expression of conditions:
  :code:`find_files(".", is_dir & matches("*.D") )`	
- Structs: :code:`s = struct(foo=2, bar=3); print(s.foo, s.bar)`
