# Makefile for simple installation of the Posetta Python Library

# Programs and directories
DOCSDIR = $(CURDIR)/documents/docs

# Define phony targets (targets that are not files)
.PHONY: develop install format test typing doc

# Install in developer mode (no need to reinstall after changing source)
develop:
	flit install -s

# Regular install, freezes the code so must reinstall after changing source code
install:
	flit install --deps production

# Format code
format:
	black .

# Run tests
test:
	pytest --cov=posetta --cov-report=term-missing

typing:
	mypy --ignore-missing-imports --disallow-untyped-defs --disallow-untyped-calls posetta

# Create documentation
doc:
	( cd $(DOCSDIR) && make html )
