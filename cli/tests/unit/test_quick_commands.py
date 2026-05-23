"""Unit tests for top-level embed, fill, run, batch commands."""
import sys
import argparse
import pytest
from unittest.mock import patch, MagicMock, AsyncMock


def _mock_mapper(mock_pipeline):
    mod = MagicMock()
    mod.PDFPipeline = MagicMock(return_value=mock_pipeline)
    mod.MapperConfig = MagicMock()
    mod.MapperConfig.from_env.return_value = MagicMock()
    return mod


def _pipeline_run_all_result(embedded="/tmp/form_embedded.pdf", filled="/tmp/form_filled.pdf"):
    return {
        "final_output": filled,
        "all_outputs": {
            "extracted_json": "/tmp/form_extracted.json",
            "mapping_json": "/tmp/form_mapped.json",
            "radio_groups": "/tmp/form_radio.json",
            "embedded_pdf": embedded,
            "filled_pdf": filled,
        },
        "timing": {"total_pipeline_seconds": 3.2},
    }


# ── embed ─────────────────────────────────────────────────────────────────────

class TestEmbed:
    def test_embed_calls_pipeline(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        schema = tmp_path / "form_keys.json"
        schema.write_text("{}")

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_run_all_result())

        args = argparse.Namespace(pdf=str(pdf), schema=str(schema), output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_embed import run
            result = run(args)
        assert result == 0
        mock_pipeline.run_all.assert_called_once()

    def test_embed_missing_pdf_returns_1(self, tmp_path):
        schema = tmp_path / "form_keys.json"
        schema.write_text("{}")
        args = argparse.Namespace(pdf="nonexistent.pdf", schema=str(schema), output=None)
        mock_pipeline = MagicMock()
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_embed import run
            result = run(args)
        assert result == 1

    def test_embed_missing_module_returns_1(self, tmp_path):
        args = argparse.Namespace(pdf="form.pdf", schema="schema.json", output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": None}):
            from pdf_autofillr_cli import cmd_embed
            import importlib
            importlib.reload(cmd_embed)
            result = cmd_embed.run(args)
        assert result == 1


# ── fill ──────────────────────────────────────────────────────────────────────

class TestFill:
    def test_fill_with_json_file(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")
        data = tmp_path / "data.json"
        data.write_text('{"first_name": "Jane"}')

        mock_pipeline = MagicMock()
        mock_pipeline.fill = AsyncMock(return_value={"output_file": "/tmp/form_filled.pdf"})

        args = argparse.Namespace(pdf=str(pdf), data=str(data), output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_fill import run
            result = run(args)
        assert result == 0
        mock_pipeline.fill.assert_called_once()

    def test_fill_no_embedded_pdf_returns_1(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        data = tmp_path / "data.json"
        data.write_text('{"name": "Jane"}')

        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf=str(pdf), data=str(data), output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_fill import run
            result = run(args)
        assert result == 1

    def test_fill_inline_json(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        mock_pipeline.fill = AsyncMock(return_value={"output_file": "/tmp/filled.pdf"})

        args = argparse.Namespace(pdf=str(pdf), data='{"name": "Jane"}', output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_fill import run
            result = run(args)
        assert result == 0

    def test_fill_invalid_json_returns_1(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf=str(pdf), data="not-a-file-not-json", output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_fill import run
            result = run(args)
        assert result == 1


# ── run ───────────────────────────────────────────────────────────────────────

class TestRun:
    def test_run_calls_pipeline(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        schema = tmp_path / "form_keys.json"
        schema.write_text("{}")
        data = tmp_path / "data.json"
        data.write_text('{"name": "Jane"}')

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_run_all_result())

        args = argparse.Namespace(pdf=str(pdf), schema=str(schema), data=str(data), output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_run import run
            result = run(args)
        assert result == 0
        mock_pipeline.run_all.assert_called_once()

    def test_run_missing_pdf_returns_1(self, tmp_path):
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
        mock_pipeline = MagicMock()
        args = argparse.Namespace(pdf="nope.pdf", schema=str(schema), data="data.json", output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_run import run
            result = run(args)
        assert result == 1

    def test_run_missing_module_returns_1(self):
        args = argparse.Namespace(pdf="form.pdf", schema="schema.json", data="data.json", output=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": None}):
            from pdf_autofillr_cli import cmd_run
            import importlib
            importlib.reload(cmd_run)
            result = cmd_run.run(args)
        assert result == 1


# ── batch ─────────────────────────────────────────────────────────────────────

class TestBatch:
    def test_batch_fills_all_json_files(self, tmp_path):
        template = tmp_path / "form.pdf"
        template.write_bytes(b"%PDF")
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
        input_dir = tmp_path / "data"
        input_dir.mkdir()
        for i in range(3):
            (input_dir / f"person_{i}.json").write_text(f'{{"name": "Person {i}"}}')
        output_dir = tmp_path / "output"

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_run_all_result(
            embedded=str(tmp_path / "form_embedded.pdf")
        ))
        mock_pipeline.fill = AsyncMock(return_value={"output_file": "/tmp/filled.pdf"})

        args = argparse.Namespace(
            template=str(template), schema=str(schema),
            input=str(input_dir), output=str(output_dir),
        )
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_batch import run
            result = run(args)
        assert result == 0
        assert mock_pipeline.fill.call_count == 3

    def test_batch_no_json_files_returns_1(self, tmp_path):
        template = tmp_path / "form.pdf"
        template.write_bytes(b"%PDF")
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        mock_pipeline = MagicMock()
        args = argparse.Namespace(
            template=str(template), schema=str(schema),
            input=str(empty_dir), output=str(tmp_path / "output"),
        )
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_batch import run
            result = run(args)
        assert result == 1

    def test_batch_partial_failure_returns_1(self, tmp_path):
        template = tmp_path / "form.pdf"
        template.write_bytes(b"%PDF")
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
        input_dir = tmp_path / "data"
        input_dir.mkdir()
        (input_dir / "good.json").write_text('{"name": "Jane"}')
        (input_dir / "bad.json").write_text('{"name": "Error"}')

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_run_all_result())
        mock_pipeline.fill = AsyncMock(side_effect=[
            {"output_file": "/tmp/good.pdf"},
            Exception("fill failed"),
        ])

        args = argparse.Namespace(
            template=str(template), schema=str(schema),
            input=str(input_dir), output=str(tmp_path / "output"),
        )
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper(mock_pipeline)}):
            from pdf_autofillr_cli.cmd_batch import run
            result = run(args)
        assert result == 1
