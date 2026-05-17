#ai-assisted with OCA/OpenAI Model with human supervision

SHELL := /bin/bash
UV ?= uv
UV_CACHE_DIR ?= /tmp/uv-cache
UV_PROJECT_ENVIRONMENT ?= /tmp/llm-prompts-venv
PYTHONPATH := src
SKILLS_ARGS ?= --skills skills
ROOT_ARGS ?= --home

.DEFAULT_GOAL := help

.PHONY: help lock test lint check list sync dry-run-delete

help:
	@printf '%s\n' 'Targets:'
	@printf '  %-16s %s\n' 'lock' 'Update uv.lock.'
	@printf '  %-16s %s\n' 'test' 'Run unit tests.'
	@printf '  %-16s %s\n' 'lint' 'Run syntax/import checks.'
	@printf '  %-16s %s\n' 'check' 'Run all validation gates.'
	@printf '  %-16s %s\n' 'list' 'List source and installed skills.'
	@printf '  %-16s %s\n' 'sync' 'Sync skills into Claude and Codex.'
	@printf '  %-16s %s\n' 'dry-run-delete' 'Preview deleting SKILL from installed locations.'

lock:
	UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) lock

test:
	UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENVIRONMENT) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(UV) run python -m unittest discover -s tests -v

lint:
	UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENVIRONMENT) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(UV) run python scripts/check_syntax.py

check: lint test

list:
	UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENVIRONMENT) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(UV) run python -m skills_manager list $(ROOT_ARGS) $(SKILLS_ARGS)

sync:
	UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENVIRONMENT) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(UV) run python -m skills_manager sync $(ROOT_ARGS) $(SKILLS_ARGS)

dry-run-delete:
	@test -n "$(SKILL)" || { echo 'ERROR: pass SKILL=<skill-name>'; exit 1; }
	UV_CACHE_DIR=$(UV_CACHE_DIR) UV_PROJECT_ENVIRONMENT=$(UV_PROJECT_ENVIRONMENT) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(PYTHONPATH) $(UV) run python -m skills_manager delete "$(SKILL)" $(ROOT_ARGS) $(SKILLS_ARGS) --dry-run
