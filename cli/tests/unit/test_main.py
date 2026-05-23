"""Unit tests for main parser, status, and setup commands."""
import sys
import pytest
# from unittest.mock import patch, MagicMock
from unittest.mock import patch
from pdf_autofillr_cli.main import build_parser, main


class TestParser:
    def test_no_args_exits_zero(self):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["pdf-autofillr"]):
                main()
        assert exc.value.code == 0

    def test_version_flag(self):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["pdf-autofillr", "--version"]):
                main()
        assert exc.value.code == 0

    def test_all_subcommands_registered(self):
        parser = build_parser()
        subparser_action = next(
            a for a in parser._subparsers._actions
            if hasattr(a, "choices") and a.choices
        )
        commands = list(subparser_action.choices.keys())
        for expected in ["status", "setup", "rag", "chatbot", "mapper", "doc-upload", "plugins"]:
            assert expected in commands

    def test_help_flag(self):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["pdf-autofillr", "--help"]):
                main()
        assert exc.value.code == 0


class TestStatusCommand:
    def test_status_dispatches_via_func(self):
        # Patch the run function on cmd_status so dispatch is verified
        with patch("pdf_autofillr_cli.cmd_status.run", return_value=0) as mock_run:
            with patch("sys.argv", ["pdf-autofillr", "status"]):
                with pytest.raises(SystemExit) as exc:
                    main()
            assert exc.value.code == 0
            mock_run.assert_called_once()

    def test_status_fallback_when_no_umbrella(self):
        from pdf_autofillr_cli.cmd_status import _fallback_status
        _fallback_status()  # must not raise

    def test_status_with_path_arg(self):
        parser = build_parser()
        args = parser.parse_args(["status", "--path", "/tmp"])
        assert args.path == "/tmp"


class TestSetupCommand:
    def test_setup_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["setup"])
        assert args.module == "all"
        assert args.force is False
        assert args.path == "."

    def test_setup_force_flag(self):
        args = build_parser().parse_args(["setup", "--force"])
        assert args.force is True

    def test_setup_module_filter(self):
        for mod in ["rag", "chatbot", "mapper", "doc-upload", "all"]:
            args = build_parser().parse_args(["setup", "--module", mod])
            assert args.module == mod

    def test_setup_no_modules_returns_1(self):
        from pdf_autofillr_cli.cmd_setup import run
        import argparse
        args = argparse.Namespace(path=".", force=False, module="all")
        # Simulate none of the modules installed by making their imports raise
        with patch.dict(sys.modules, {
            "ragpdf": None,
            "ragpdf.entrypoints": None,
            "ragpdf.entrypoints.setup": None,
            "chatbot": None,
            "chatbot.entrypoints": None,
            "chatbot.entrypoints.cli": None,
            "pdf_autofillr_mapper": None,
            "pdf_autofillr_mapper.entrypoints": None,
            "pdf_autofillr_mapper.entrypoints.cli": None,
            "pdf_autofillr_doc_upload": None,
            "pdf_autofillr_doc_upload.entrypoints": None,
            "pdf_autofillr_doc_upload.entrypoints.cli": None,
        }):
            result = run(args)
        assert result == 1
