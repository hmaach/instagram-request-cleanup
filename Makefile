# instagram-request-cleanup Makefile (cross-platform)

PYTHON := python3
VENV := venv

ifeq ($(OS),Windows_NT)
    ACTIVATE = $(VENV)\Scripts\activate
    PIP = $(VENV)\Scripts\pip
    PY = $(VENV)\Scripts\python
else
    ACTIVATE = . $(VENV)/bin/activate
    PIP = $(VENV)/bin/pip
    PY = $(VENV)/bin/python
endif

.PHONY: all venv install browsers run clean

all: install browsers

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install playwright

browsers:
	$(PY) -m playwright install

run:
	$(PY) main.py

clean:
	rm -rf $(VENV)