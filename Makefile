# Makefile for simple installation of the Posetta Python Library
#
# Authors:
# --------
#
# * Geir Arne Hjelle <geir.arne.hjelle@kartverket.no>
#

# Programs and directories
DOCSDIR = $(CURDIR)/documents/docs

# Define phony targets (targets that are not files)
.PHONY: develop install doc test

# Install in developer mode (no need to reinstall after changing source)
develop:
	flit install -s

# Regular install, freezes the code so must reinstall after changing source code
install:
	flit install --deps production


# Create documentation
doc:
	( cd $(DOCSDIR) && make html )

# Run tests
test:
	( cd posetta && py.test --doctest-modules )

