# pdf-autofillr-cli — Makefile

.PHONY: help install install-all test test-unit test-integration test-coverage benchmark build clean

help:
	@echo ""
	@echo "pdf-autofillr-cli"
	@echo "================="
	@echo "  install           pip install -e .[dev]"
	@echo "  install-all       install CLI + all pdf-autofillr modules"
	@echo "  test              run all 69 tests"
	@echo "  test-unit         unit tests only (no modules needed)"
	@echo "  test-integration  parser integration tests"
	@echo "  test-coverage     tests with coverage report"
	@echo "  benchmark         run benchmarking suite"
	@echo "  build             build wheel and sdist"
	@echo "  clean             remove build artifacts and cache"
	@echo ""

install:
	cd cli && pip install -e ".[dev]"

install-all:
	cd cli && pip install -e ".[all,dev]"

test:
	cd cli && pytest tests/ --tb=short -q

test-unit:
	cd cli && pytest tests/unit/ -v

test-integration:
	cd cli && pytest tests/integration/ -v

test-coverage:
	cd cli && pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing

benchmark:
	python benchmarks/run_benchmark.py

build:
	cd cli && pip install build && python -m build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "coverage.xml" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	@echo "Clean complete"