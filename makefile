.ONESHELL:

SHELL := /bin/bash
# define the name of the virtual environment directory
VENV := .venv
PYTHON := python3
PIP_VENV := $(VENV)/bin/pip3
PYTHON_VENV := $(VENV)/bin/python3
MAIN_DIR := 'src'


# define the console colors
COLOR_RESET  = \033[0m
COLOR_GREEN  = \033[32m
COLOR_YELLOW = \033[33m
COLOR_RED    = \033[31m

#################################### Functions ###########################################

# Function to create python virtualenv if it doesn't exist
define create-venv
	@if [ ! -d $(VENV) ]; then \
		echo -e "${COLOR_YELLOW}Creating virtual environment...${COLOR_RESET}"; \
		$(PYTHON) -m venv $(VENV); \
	else \
		echo -e "${COLOR_GREEN}Virtual environment already exists...${COLOR_RESET}"; \
	fi
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo -e "${COLOR_RED}Source virtual environment before running the app...${COLOR_RESET}"; \
		echo -e "${COLOR_RED}Manually run: \`source $(VENV)/bin/activate\`${COLOR_RESET}"; \
	else \
		echo -e "${COLOR_GREEN}Virtual environment is activated. Proceeding with installation.${COLOR_RESET}"; \
	fi
endef


setup: ## Install the package in development mode including all dependencies inside a virtualenv (container).
	@if [ ! -d $(VENV) ]; then \
		echo -e "${COLOR_RED}Virtual environment not found. Please run 'make venv' before running 'make setup'${COLOR_RESET}"; \
		exit 1; \
	fi
	@echo -e "${COLOR_YELLOW}Checking if virtual environment is activated...${COLOR_RESET}"
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo -e "${COLOR_RED}Virtual environment is not activated. Please run 'make venv' before running 'make setup'.${COLOR_RESET}"; \
		exit 1; \
	fi
	@echo -e "${COLOR_YELLOW}Virtual environment is activated. Proceeding with setup.${COLOR_RESET}"
	@echo -e "\n"
	@echo -e "${COLOR_YELLOW}Upgrading pip to latest version...${COLOR_RESET}"
	${PYTHON_VENV} -m pip install --upgrade pip
	@echo -e "${COLOR_YELLOW}Installing dependencies...${COLOR_RESET}"
	$(PIP_VENV) install -r requirements.txt
	@echo -e "${COLOR_YELLOW}Installing pre-commit...${COLOR_RESET}"
	export PRE_COMMIT_HOME=./$(VENV)/.cache/pre-commit
	pre-commit install
	@echo -e "${COLOR_GREEN}Setup completed...${COLOR_RESET}"

venv:  ## Create virtualenv environment on local directory.
	@$(create-venv)

# -------------------------------------- Project Execution -------------------------------
run:  ## Run Python app
	$(PYTHON_VENV) -m $(MAIN_DIR)

# -------------------------------------- Test Execution ---------------------------------
test: ## Run tests quickly with pytest
	${PYTHON_VENV} -m pytest -v --color=yes tests

# -------------------------------------- Clean Up  --------------------------------------
.PHONY: clean
clean: deactivate clean-pyc clean-test clean-logs clean-pre-commit clean-venv clean-ruff-cache

deactivate: ## Deactivate virtual environment
	@echo -e "${COLOR_YELLOW}Checking if virtual environment is still active...${COLOR_RESET}"
	@if [ "$$VIRTUAL_ENV" ]; then \
	echo -e "${COLOR_RED}Please run 'deactivate' to deactivate the virtual environment before running 'make clean'.${COLOR_RESET}"; \
		exit 1; \
	else \
		echo -e "${COLOR_GREEN}Virtual environment is not active. Proceeding with clean up.${COLOR_RESET}"; \
	fi

clean-venv: ## Remove virtual environment
	@echo -e "${COLOR_YELLOW}Removing virtual environment $(VENV)...${COLOR_RESET}"
	rm -fr $(VENV)

clean-pyc: ## Remove Python file artifacts
	@echo -e "${COLOR_YELLOW}Removing Python file artifacts...${COLOR_RESET}"
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Remove test and coverage artifacts
	@echo -e "${COLOR_YELLOW}Removing test and coverage artifacts...${COLOR_RESET}"
	rm -fr .tox/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-logs: ## Remove logs
	@echo -e "${COLOR_YELLOW}Removing logs...${COLOR_RESET}"
	find . -name '*.log' -exec rm -rf {} +

clean-pre-commit: ## Remove pre-commit artifacts
	@echo -e "${COLOR_YELLOW}Removing pre-commit artifacts...${COLOR_RESET}"
	rm -fr .git/hooks/pre-commit

clean-ruff-cache: ## Remove ruff cache
	@echo -e "${COLOR_YELLOW}Removing ruff cache...${COLOR_RESET}"
	rm -fr .ruff_cache
