"""Unit tests for mapper, doc-upload, and plugins CLI commands."""
import sys
import json
import argparse
import pytest
from unittest.mock import patch, MagicMock, AsyncMock


# ── helpers ───────────────────────────────────────────────────────────────────

def _mock_mapper_mod(mock_pipeline):
    mod = MagicMock()
    mod.PDFPipeline = MagicMock(return_value=mock_pipeline)
    mod.MapperConfig = MagicMock()
    mod.MapperConfig.from_env.return_value = MagicMock()
    return mod


def _mock_doc_module():
    mod = MagicMock()
    client = MagicMock()
    client.run.return_value = {
        "output_flat": {"name": "Jane", "email": "jane@example.com"},
        "success": True,
        "filled_pdf_path": "/tmp/filled.pdf",
    }
    mod.DocUploadClient = MagicMock(return_value=client)
    return mod, client


def _mock_plugins_module(mock_manager_instance):
    mod = MagicMock()
    mod.PluginManager = MagicMock(return_value=mock_manager_instance)
    return mod


def _pipeline_embed_result():
    return {
        "final_output": "/tmp/form_filled.pdf",
        "all_outputs": {"embedded_pdf": "/tmp/form_embedded.pdf"},
        "timing": {"total_pipeline_seconds": 2.1},
    }


def _pipeline_fill_result():
    return {"output_file": "/tmp/form_filled.pdf"}


# ── Mapper embed ──────────────────────────────────────────────────────────────

class TestMapperEmbed:
    def test_embed_calls_pipeline(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        schema = tmp_path / "schema.json"
        schema.write_text("{}")

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_embed_result())

        args = argparse.Namespace(
            pdf=str(pdf), schema=str(schema),
            mapper_command="embed", user="default",
        )
        from pdf_autofillr_cli.cmd_mapper import _embed
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = _embed(args)
        assert result == 0
        mock_pipeline.run_all.assert_called_once()

    def test_embed_no_embedded_pdf_key_still_ok(self, tmp_path):
        """run_all always returns all_outputs with embedded_pdf."""
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        schema = tmp_path / "schema.json"
        schema.write_text("{}")

        mock_pipeline = MagicMock()
        mock_pipeline.run_all = AsyncMock(return_value=_pipeline_embed_result())

        from pdf_autofillr_cli.cmd_mapper import _embed
        args = argparse.Namespace(pdf=str(pdf), schema=str(schema),
                                  mapper_command="embed", user="default")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = _embed(args)
        assert result == 0


# ── Mapper fill ───────────────────────────────────────────────────────────────

class TestMapperFill:
    def test_fill_with_json_file(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")
        data = tmp_path / "data.json"
        data.write_text('{"investor_name": "Jane"}')

        mock_pipeline = MagicMock()
        mock_pipeline.fill = AsyncMock(return_value=_pipeline_fill_result())

        from pdf_autofillr_cli.cmd_mapper import _fill
        args = argparse.Namespace(pdf=str(pdf), data=str(data), user="default")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = _fill(args)
        assert result == 0
        mock_pipeline.fill.assert_called_once()

    def test_fill_no_embedded_returns_1(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        data = tmp_path / "data.json"
        data.write_text('{"name": "Jane"}')

        mock_pipeline = MagicMock()
        from pdf_autofillr_cli.cmd_mapper import _fill
        args = argparse.Namespace(pdf=str(pdf), data=str(data), user="default")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = _fill(args)
        assert result == 1

    def test_fill_inline_json(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        mock_pipeline.fill = AsyncMock(return_value=_pipeline_fill_result())

        from pdf_autofillr_cli.cmd_mapper import _fill
        args = argparse.Namespace(pdf=str(pdf), data='{"name": "Jane"}', user="default")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = _fill(args)
        assert result == 0

    def test_fill_invalid_json_raises(self, tmp_path):
        pdf = tmp_path / "form.pdf"
        pdf.write_bytes(b"%PDF")
        embedded = tmp_path / "form_embedded.pdf"
        embedded.write_bytes(b"%PDF")

        mock_pipeline = MagicMock()
        from pdf_autofillr_cli.cmd_mapper import _fill
        args = argparse.Namespace(pdf=str(pdf), data="not-a-file-not-json", user="default")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            with pytest.raises(json.JSONDecodeError):
                _fill(args)


# ── Mapper run dispatch ───────────────────────────────────────────────────────

class TestMapperRun:
    def test_no_subcommand_returns_1(self):
        from pdf_autofillr_cli.cmd_mapper import run as mapper_run
        mock_pipeline = MagicMock()
        args = argparse.Namespace(mapper_command=None)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": _mock_mapper_mod(mock_pipeline)}):
            result = mapper_run(args)
        assert result == 1


# ── Doc Upload ────────────────────────────────────────────────────────────────

class TestDocUploadProcess:
    def test_process_calls_client_run(self):
        fake_mod, mock_client = _mock_doc_module()
        args = argparse.Namespace(
            doc="investor.pdf",
            pdf="blank.pdf",
            schema_keys_path="configs/form_keys.json",
            user_id="u1",
            pdf_doc_id="lp_v1",
        )
        from pdf_autofillr_cli.cmd_doc_upload import _process
        with patch.dict(sys.modules, {"pdf_autofillr_doc_upload": fake_mod}):
            result = _process(args)
        assert result == 0
        mock_client.run.assert_called_once()

    def test_process_shows_field_count(self, capsys):
        fake_mod, mock_client = _mock_doc_module()
        args = argparse.Namespace(
            doc="investor.pdf", pdf="blank.pdf",
            schema_keys_path="form_keys.json",
            user_id="u1", pdf_doc_id="lp_v1",
        )
        from pdf_autofillr_cli.cmd_doc_upload import _process
        with patch.dict(sys.modules, {"pdf_autofillr_doc_upload": fake_mod}):
            _process(args)
        out = capsys.readouterr().out
        assert "2" in out  # 2 fields in mock


class TestDocUploadRun:
    def test_no_subcommand_returns_1(self):
        fake_mod, _ = _mock_doc_module()
        args = argparse.Namespace(doc_command=None)
        from pdf_autofillr_cli.cmd_doc_upload import run as doc_run
        with patch.dict(sys.modules, {"pdf_autofillr_doc_upload": fake_mod}):
            result = doc_run(args)
        assert result == 1


# ── Plugins ───────────────────────────────────────────────────────────────────

class TestPluginsList:
    def test_list_no_plugins(self, capsys):
        args = argparse.Namespace(path=None, category=None, as_json=False)
        mock_mgr = MagicMock()
        mock_mgr.list_plugins.return_value = {}
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import _list
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _list(args)
        assert result == 0

    def test_list_as_json(self, capsys):
        args = argparse.Namespace(path=None, category=None, as_json=True)
        mock_mgr = MagicMock()
        mock_mgr.list_plugins.return_value = {"validator": ["email-validator"]}
        mock_mgr.get_plugin_info.return_value = {
            "name": "email-validator", "version": "1.0.0", "description": "Email validator"
        }
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import _list
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _list(args)
        assert result == 0
        data = json.loads(capsys.readouterr().out)
        assert "validator" in data

    def test_list_with_plugins(self, capsys):
        args = argparse.Namespace(path=None, category=None, as_json=False)
        mock_mgr = MagicMock()
        mock_mgr.list_plugins.return_value = {"extractor": ["invoice-extractor"]}
        mock_mgr.get_plugin_info.return_value = {
            "name": "invoice-extractor", "version": "1.0.0", "description": "Invoice extractor",
        }
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import _list
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _list(args)
        assert result == 0
        assert "invoice-extractor" in capsys.readouterr().out


class TestPluginsInfo:
    def test_info_found(self, capsys):
        args = argparse.Namespace(name="email-validator", category=None)
        mock_mgr = MagicMock()
        mock_mgr.get_plugin_info.return_value = {"name": "email-validator", "version": "1.0.0"}
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import _info
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _info(args)
        assert result == 0
        assert "email-validator" in capsys.readouterr().out

    def test_info_not_found(self):
        args = argparse.Namespace(name="nonexistent", category=None)
        mock_mgr = MagicMock()
        mock_mgr.get_plugin_info.return_value = None
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import _info
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _info(args)
        assert result == 1


class TestPluginsRun:
    def test_no_subcommand_returns_1(self):
        args = argparse.Namespace(plugins_command=None)
        mock_mgr = MagicMock()
        mock_mgr.list_plugins.return_value = {}
        fake_mod = _mock_plugins_module(mock_mgr)
        from pdf_autofillr_cli.cmd_plugins import run as plugins_run
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = plugins_run(args)
        assert result == 1
