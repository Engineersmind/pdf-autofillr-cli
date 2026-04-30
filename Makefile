# pdf-autofillr-cli — Makefile

.PHONY: help install install-all test test-unit test-integration clean build publish

help:
	@echo ""
	@echo "pdf-autofillr-cli"
	@echo "================="
	@echo "  install          pip install -e .[dev]"
	@echo "  install-all      install CLI + all pdf-autofillr modules"
	@echo "  test             run all 69 tests"
	@echo "  test-unit        unit tests only (no modules needed)"
	@echo "  test-integration parser integration tests"
	@echo "  build            build distribution packages"
	@echo "  publish          upload to PyPI (requires twine)"
	@echo "  clean            remove build artefacts"
	@echo ""

install:
	cd packages/cli && pip install -e ".[dev]"

install-all:
	cd packages/cli && pip install -e ".[all,dev]"

test:
	cd packages/cli && pytest tests/ -v

test-unit:
	cd packages/cli && pytest tests/unit/ -v

test-integration:
	cd packages/cli && pytest tests/integration/ -v

test-coverage:
	cd packages/cli && pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing

benchmark:
	python benchmarks/run_benchmark.py

build:
	cd packages/cli && pip install build && python -m build

publish:
	cd packages/cli && twine upload dist/*

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"
