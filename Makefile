#   Makefile wrapper for greenland4 development
#   Copyright (C) 2018 M E Leypold
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see
#   <https://www.gnu.org/licenses/>.
#

_default: check doc
-include  META/Rules.mk

PY-SOURCES = $(shell find lib/greenland -name '*.py' | grep -v '/test/' | grep -v '/sketches/' )

check:: pytest typecheck

pytest:: 
	cd lib && pytest --basetemp="$(CURDIR)/.tmp"

typecheck:
	@echo
	MYPYPATH=$(wildcard .pyenv3/lib/python3.*/site-packages) mypy --follow-imports=silent $(PY-SOURCES)
	@echo

flake8check:
	@echo
	flake8 --ignore=E501,E251,E221 lib
	@echo

doc::
	cd lib && make latexpdf
	cd lib && make html
	cp lib/_build/latex/Greenland.pdf greenland-manual.pdf
clean::
	find . -name '*~' | xargs rm -f
	find . \( -name '.pyenv*' -type d -prune \) -o \( \( -name __pycache__ -o -name .pytest_cache \) -a -print \) | xargs rm -rf
	rm -rf .build
	cd lib && make clean

	find . -name '.tmp' | xargs rm -rf

cleaner:: clean
	find . -name '*.egg-info' -type d    | xargs rm -rf
	find . -name '.pytest_cache' -type d | xargs rm -rf
	find . -name '*__pycache__*' -type d | xargs rm -rf
	rm -rf dist build lib/.mypy_cache

install-linked::
	pip install -e .

install-independently::
	pip install .

INSTALL-METHOD ?= independently

install: install-$(INSTALL-METHOD)
