.PHONY: install install-dev run test lint clean

# -----------------------------------------------------------------------------
# OS Detection
# -----------------------------------------------------------------------------

ifeq ($(OS),Windows_NT)
    PLATFORM := WINDOWS
else
    PLATFORM := UNIX
endif

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

PROJECT_NAME := crewai-based-multi-agent-system
UV := uv
SRC := src
TESTS := tests

# Python executable
ifeq ($(PLATFORM),WINDOWS)
    PYTHON := python
else
    PYTHON := python3
endif

# -----------------------------------------------------------------------------
# Platform-specific commands & logging
# -----------------------------------------------------------------------------

ifeq ($(PLATFORM),WINDOWS)

	# Windows-safe logging (no ANSI, no printf)
    define log
		@rem
    endef

    define success
		@rem
    endef

    RM := rmdir /s /q
    CLEAN_PYCACHE := for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
    CLEAN_PYTEST := for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rmdir /s /q "%%d"
    CLEAN_RUFF := for /d /r . %%d in (.ruff_cache) do @if exist "%%d" rmdir /s /q "%%d"

else

	# POSIX logging with colors
    BLUE := \033[36m
    GREEN := \033[32m
    RESET := \033[0m

    define log
	@printf "$(BLUE)==> %s$(RESET)\n" "$(1)"
    endef

    define success
	@printf "$(GREEN)✔ %s$(RESET)\n" "$(1)"
    endef

    RM := rm -rf
    CLEAN_PYCACHE := find . -type d -name "__pycache__" -exec rm -rf {} +
    CLEAN_PYTEST := find . -type d -name ".pytest_cache" -exec rm -rf {} +
    CLEAN_RUFF := find . -type d -name ".ruff_cache" -exec rm -rf {} +

endif

# -----------------------------------------------------------------------------
# Command line target arguments
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Core Environment Setup
# -----------------------------------------------------------------------------

.PHONY: install sync update lock clean

install:	## Create virtualenv and install dependencies
	$(call log,Setting up virtual environment and installing dependencies...)
	$(UV) venv --clear
	$(UV) sync
	$(call success,Environment ready)

sync: 		## Sync environment with lockfile
	$(call log,Syncing environment with lockfile...)
	$(UV) sync
	$(call success,Sync complete)

update:		## Upgrade dependencies and refresh lockfile
	$(call log,Upgrading dependencies and refreshing lockfile...)
	$(UV) lock --upgrade
	$(UV) sync
	$(call success,Dependencies updated)

lock:		## Generate/update lockfile without upgrading
	$(call log,Generating lockfile...)
	$(UV) lock
	$(call success,Lockfile updated)

clean:		## Remove virtualenv, builds & caches
	$(call log,Cleaning environment, builds and caches...)
	-$(RM) .venv
	-$(RM) dist
	-$(CLEAN_PYCACHE)
	-$(CLEAN_PYTEST)
	-$(CLEAN_RUFF)
	$(call success,Clean complete)

# -----------------------------------------------------------------------------
# Development
# -----------------------------------------------------------------------------

.PHONY: run exec shell

run: 		## Run application
	$(call log,Running application...)
	$(UV) run $(PYTHON) app.py

exec:		## Execute python script. Usage: make exec path/to/script.py [args...]
ifndef FILE
	$(error Usage: make exec FILE=path/to/script.py ARGS="--flags")
endif
	$(call log,Executing $(FILE)...)
	$(UV) run $(PYTHON) $(FILE) $(ARGS)

shell:		## Spawn shell inside uv environment
	$(call log,Opening shell...)
ifeq ($(PLATFORM),WINDOWS)
	$(UV) run cmd
else
	$(UV) run bash
endif

# -----------------------------------------------------------------------------
# Testing & Quality
# -----------------------------------------------------------------------------

.PHONY: test lint format check

test: 		## Run tests
	$(call log,Running tests...)
	$(UV) run pytest $(TESTS)
	$(call success,Tests completed)

lint: 		## Run linting (ruff)
	$(call log,Running linter...)
	$(UV) run ruff check $(SRC) $(TESTS)

lint-fix:	## Run linting (ruff) & fix
	$(call log,Running linter...)
	$(UV) run ruff check $(SRC) $(TESTS) --fix

format: 	## Auto-format code
	$(call log,Formatting code...)
	$(UV) run ruff format $(SRC) $(TESTS)
	$(call success,Formatting complete)

check: 		lint test ## Run all checks
	$(call log,All checks passed)

# -----------------------------------------------------------------------------
# Type Checking
# -----------------------------------------------------------------------------

.PHONY: typecheck

typecheck: 	## Run mypy
	$(call log,Running type checks...)
	$(UV) run mypy $(SRC)

# -----------------------------------------------------------------------------
# Build & Distribution
# -----------------------------------------------------------------------------

.PHONY: build publish

build:		## Build package
	$(call log,Building package...)
	$(UV) build
	$(call success,Build complete)

publish:	## Publish to PyPI
	$(call log,Publishing package...)
	$(UV) publish
	$(call success,Publish complete)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

.PHONY: deps tree

deps:		## Show installed dependencies
	$(call log, Listing dependencies...)
	$(UV) pip list

tree:		## Show dependency tree
	$(call log,Displaying dependency tree...)
	$(UV) pip tree

# -----------------------------------------------------------------------------
# Help
# -----------------------------------------------------------------------------

.PHONY: help

help:		## Show this help
ifeq ($(PLATFORM),WINDOWS)
	@echo Available commands:
	@findstr /R "^[a-zA-Z_-]*:" $(MAKEFILE_LIST)
else
	@printf "\033[33mAvailable commands:\033[0m\n"
	@grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST)
endif
