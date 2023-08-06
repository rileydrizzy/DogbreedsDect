.DEFAULT_GOAL := help

help:
	@echo "    prepare              desc of the command prepare"
	@echo "    install              desc of the command install"


install:
	@echo "Installing..."
	python -m pip install -r requirements.txt
	pre-commit install
	
# Define the path to the virtual environment
VENV_DIR := env

# Define the activation command based on the operating system
ifdef OS
    ifeq ($(OS),Windows_NT)
        ACTIVATE_CMD := $(VENV_DIR)\Scripts\activate
    else
        ACTIVATE_CMD := source $(VENV_DIR)/bin/activate
    endif
else
    ACTIVATE_CMD := source $(VENV_DIR)/bin/activate
endif

.PHONY: activate

activate:
	#@echo "Activating virtual environment"
	$(ACTIVATE_CMD)

setup: activate install 

precommit:
	@echo "Running precommit on all files"
	pre-commit run --all-files

export:
	@echo "Exporting dependencies to requirements file"
	python -m pip freeze > requirements.txt

force backup: # To push to Github without running precommit
	git commit --no-verify -m "backup"
	git push origin main