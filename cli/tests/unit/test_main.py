"""Unit tests for main parser and status command."""

from unittest.mock import patch

import pytest

from pdf_autofillr_cli.main import build_parser, main


class TestParser:
    def test_no_args_exits_zero(self):
        with pytest.raises(SystemExit) as exc, patch("sys.argv", ["pdf-autofillr-cli"]):
            main()
        assert exc.value.code == 0

    def test_version_flag(self):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["pdf-autofillr-cli", "--version"]):
                main()
        assert exc.value.code == 0

    def test_help_flag(self):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["pdf-autofillr-cli", "--help"]):
                main()
        assert exc.value.code == 0

    def test_all_subcommands_registered(self):
        parser = build_parser()
        subparser_action = next(
            a for a in parser._subparsers._actions if hasattr(a, "choices") and a.choices
        )
        commands = list(subparser_action.choices.keys())
        for expected in [
            "embed",
            "fill",
            "run",
            "batch",
            "chatbot",
            "doc-upload",
            "mapper",
            "rag",
            "plugins",
            "status",
            "setup",
        ]:
            assert expected in commands

    def test_invalid_command_exits(self):
        with pytest.raises(SystemExit):
            with patch("sys.argv", ["pdf-autofillr-cli", "nonexistent"]):
                main()


class TestStatusCommand:
    def test_status_dispatches(self):
        with patch("pdf_autofillr_cli.cmd_status.run", return_value=0) as mock_run:
            with patch("sys.argv", ["pdf-autofillr-cli", "status"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 0
            mock_run.assert_called_once()

    def test_status_runs_without_modules(self):
        """Status should never crash even if nothing is installed."""
        import argparse

        from pdf_autofillr_cli.cmd_status import run

        run(argparse.Namespace())
