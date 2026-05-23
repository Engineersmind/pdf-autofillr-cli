"""Unit tests for status and setup commands."""
import os
import argparse
import pytest
from unittest.mock import patch


class TestStatus:
    def test_status_runs_without_crash(self):
        from pdf_autofillr_cli.cmd_status import run
        # Should never crash regardless of what's installed
        run(argparse.Namespace())

    def test_status_no_modules_returns_1(self):
        from pdf_autofillr_cli.cmd_status import run
        import sys
        with patch.dict(sys.modules, {
            "pdf_autofillr_mapper": None,
            "chatbot": None,
            "pdf_autofillr_doc_upload": None,
            "ragpdf": None,
            "pdf_autofillr_plugins": None,
        }):
            with patch.dict(os.environ, {}, clear=True):
                result = run(argparse.Namespace())
        assert result == 1

    def test_status_with_api_key_set(self):
        from pdf_autofillr_cli.cmd_status import run
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            # Should not crash — may return 0 or 1 depending on modules
            result = run(argparse.Namespace())
        assert result in (0, 1)

    def test_status_placeholder_key_counts_as_missing(self):
        from pdf_autofillr_cli.cmd_status import run
        with patch.dict(os.environ, {"OPENAI_API_KEY": "your_openai_key_here"}, clear=True):
            result = run(argparse.Namespace())
        assert result == 1


class TestSetup:
    def test_setup_creates_env_from_example(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        env_example = tmp_path / ".env.example"
        env_example.write_text("OPENAI_API_KEY=your_key_here\n")

        from pdf_autofillr_cli.cmd_setup import run
        result = run(argparse.Namespace())
        assert result == 0
        assert (tmp_path / ".env").exists()

    def test_setup_skips_if_env_exists(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".env").write_text("OPENAI_API_KEY=real-key\n")

        from pdf_autofillr_cli.cmd_setup import run
        result = run(argparse.Namespace())
        assert result == 0
        # Content should be unchanged
        assert "real-key" in (tmp_path / ".env").read_text()

    def test_setup_creates_minimal_env_without_example(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        from pdf_autofillr_cli.cmd_setup import run
        result = run(argparse.Namespace())
        assert result == 0
        assert (tmp_path / ".env").exists()
        content = (tmp_path / ".env").read_text()
        assert "OPENAI_API_KEY" in content

    def test_setup_shows_usage_path_when_found(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "USAGE.md").write_text("# Usage\n")

        from pdf_autofillr_cli.cmd_setup import run
        run(argparse.Namespace())
        captured = capsys.readouterr()
        assert "USAGE.md" in captured.out
