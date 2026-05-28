"""Unit tests for extract and validate commands."""

from __future__ import annotations

import argparse
import json
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# ── helpers ───────────────────────────────────────────────────────────────────


def _mock_mapper(mock_pipeline):
    mod = MagicMock()
    mod.PDFPipeline = MagicMock(return_value=mock_pipeline)
    mod.MapperConfig = MagicMock()
    mod.MapperConfig.from_env.return_value = MagicMock()
    return mod


# ── extract ───────────────────────────────────────────────────────────────────


class TestExtract:
    def test_extract_writes_schema_file(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        out = tmp_path / "schema.json"

        schema_data = {"first_name": {}, "last_name": {}, "dob": {}}
        mock_pipeline = MagicMock()
        mock_pipeline.extract = AsyncMock(return_value={"fields": schema_data})

        args = argparse.Namespace(pdf=str(pdf), output=str(out), pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)

        assert result == 0
        assert out.exists()
        written = json.loads(out.read_text())
        assert written == schema_data

    def test_extract_default_output_path(self, tmp_path):
        pdf = tmp_path / "myform.pdf"
        pdf.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        mock_pipeline.extract = AsyncMock(return_value={"fields": {"name": {}}})

        args = argparse.Namespace(pdf=str(pdf), output=None, pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)

        assert result == 0
        assert (tmp_path / "myform_schema.json").exists()

    def test_extract_pretty_flag(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        out = tmp_path / "schema.json"

        mock_pipeline = MagicMock()
        mock_pipeline.extract = AsyncMock(return_value={"fields": {"a": 1}})

        args = argparse.Namespace(pdf=str(pdf), output=str(out), pretty=True)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)

        assert result == 0
        raw = out.read_text()
        assert "\n" in raw  # pretty-printed

    def test_extract_missing_pdf_returns_1(self, tmp_path):
        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf="nope.pdf", output=None, pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)
        assert result == 1

    def test_extract_missing_module_returns_1(self):
        args = argparse.Namespace(pdf="form.pdf", output=None, pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": None}):
            import importlib

            from pdf_autofillr_cli import cmd_extract

            importlib.reload(cmd_extract)
            result = cmd_extract.run(args)
        assert result == 1

    def test_extract_pipeline_exception_returns_1(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        mock_pipeline.extract = AsyncMock(side_effect=RuntimeError("SDK error"))

        args = argparse.Namespace(pdf=str(pdf), output=None, pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)
        assert result == 1

    def test_extract_creates_output_directory(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        out = tmp_path / "nested" / "deep" / "schema.json"

        mock_pipeline = MagicMock()
        mock_pipeline.extract = AsyncMock(return_value={"fields": {"x": 1}})

        args = argparse.Namespace(pdf=str(pdf), output=str(out), pretty=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_extract import run

            result = run(args)

        assert result == 0
        assert out.exists()


# ── validate ──────────────────────────────────────────────────────────────────


class TestValidate:
    def _make_schema(self, tmp_path, fields: list) -> str:
        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps(fields))
        return str(schema_path)

    def test_validate_passes_when_all_fields_filled(self, tmp_path):
        pdf = tmp_path / "filled.pdf"
        pdf.write_bytes(b"%PDF")
        schema_path = self._make_schema(tmp_path, ["first_name", "last_name"])

        mock_pipeline = MagicMock()
        mock_pipeline.validate = AsyncMock(
            return_value={
                "valid": True,
                "missing": [],
                "empty": [],
                "total_required": 2,
                "filled_count": 2,
            }
        )

        args = argparse.Namespace(pdf=str(pdf), schema=schema_path, strict=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_validate import run

            result = run(args)
        assert result == 0

    def test_validate_fails_when_fields_missing(self, tmp_path):
        pdf = tmp_path / "filled.pdf"
        pdf.write_bytes(b"%PDF")
        schema_path = self._make_schema(tmp_path, ["first_name", "last_name", "dob"])

        mock_pipeline = MagicMock()
        mock_pipeline.validate = AsyncMock(
            return_value={
                "valid": False,
                "missing": ["dob"],
                "empty": [],
                "total_required": 3,
                "filled_count": 2,
            }
        )

        args = argparse.Namespace(pdf=str(pdf), schema=schema_path, strict=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_validate import run

            result = run(args)
        assert result == 1

    def test_validate_strict_fails_on_empty_fields(self, tmp_path):
        pdf = tmp_path / "filled.pdf"
        pdf.write_bytes(b"%PDF")
        schema_path = self._make_schema(tmp_path, ["first_name", "last_name"])

        mock_pipeline = MagicMock()
        mock_pipeline.validate = AsyncMock(
            return_value={
                "valid": False,
                "missing": [],
                "empty": ["last_name"],
                "total_required": 2,
                "filled_count": 1,
            }
        )

        args = argparse.Namespace(pdf=str(pdf), schema=schema_path, strict=True)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_validate import run

            result = run(args)
        assert result == 1

    def test_validate_missing_pdf_returns_1(self, tmp_path):
        schema_path = self._make_schema(tmp_path, ["a"])
        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf="nope.pdf", schema=schema_path, strict=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_validate import run

            result = run(args)
        assert result == 1

    def test_validate_missing_schema_returns_1(self, tmp_path):
        pdf = tmp_path / "filled.pdf"
        pdf.write_bytes(b"%PDF")
        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf=str(pdf), schema="nope.json", strict=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_validate import run

            result = run(args)
        assert result == 1

    def test_validate_missing_module_returns_1(self, tmp_path):
        pdf = tmp_path / "filled.pdf"
        pdf.write_bytes(b"%PDF")
        schema_path = self._make_schema(tmp_path, ["a"])
        args = argparse.Namespace(pdf=str(pdf), schema=schema_path, strict=False)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": None}):
            import importlib

            from pdf_autofillr_cli import cmd_validate

            importlib.reload(cmd_validate)
            result = cmd_validate.run(args)
        assert result == 1

    def test_validate_local_fallback_all_filled(self, tmp_path):
        """_local_validate works when pypdf is unavailable (structural check only)."""
        from pdf_autofillr_cli.cmd_validate import _local_validate

        schema = ["first_name", "last_name"]
        with patch.dict(sys.modules, {"pypdf": None}):
            result = _local_validate("any.pdf", schema, strict=False)

        # Without pypdf, falls back to structural check — always valid
        assert result["valid"] is True

    def test_validate_local_fallback_dict_schema(self, tmp_path):
        from pdf_autofillr_cli.cmd_validate import _local_validate

        schema = {"fields": ["first_name", "last_name"]}
        with patch.dict(sys.modules, {"pypdf": None}):
            result = _local_validate("any.pdf", schema, strict=False)
        assert result["valid"] is True
