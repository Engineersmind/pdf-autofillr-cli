"""Unit tests for mapper, doc-upload, and plugins CLI commands."""
import json
import sys
import argparse
import pytest
from unittest.mock import patch, MagicMock

from pdf_autofillr_cli.cmd_mapper import run as mapper_run, _embed, _fill
from pdf_autofillr_cli.cmd_doc_upload import run as doc_run, _process
from pdf_autofillr_cli.cmd_plugins import run as plugins_run, _list, _info


# ── helpers ───────────────────────────────────────────────────────────────────

def _mock_mapper_module(mock_orch):
    """Return a fake pdf_autofillr_mapper module with MapperOrchestrator."""
    mod = MagicMock()
    mod.MapperOrchestrator = MagicMock()
    mod.MapperOrchestrator.from_env.return_value = mock_orch
    return mod


def _mock_doc_module(mock_client):
    mod = MagicMock()
    mod.DocUploadClient = MagicMock()
    mod.DocUploadClient.from_env.return_value = mock_client
    return mod


def _mock_plugins_module(mock_manager_instance):
    mod = MagicMock()
    mod.PluginManager = MagicMock(return_value=mock_manager_instance)
    return mod


# ── Mapper ────────────────────────────────────────────────────────────────────

class TestMapperEmbed:
    def test_embed_calls_orchestrator(self, mock_mapper_orch):
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        args = argparse.Namespace(pdf="form.pdf", user="u1", pdf_doc_id="lp_v1")
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            result = _embed(args)
        assert result == 0
        mock_mapper_orch.make_embed_file.assert_called_once_with(
            pdf_path="form.pdf", user_id="u1", pdf_doc_id="lp_v1"
        )


class TestMapperFill:
    def test_fill_with_json_file(self, tmp_json, mock_mapper_orch):
        data_path = tmp_json("data.json", {"investor_name": "Jane"})
        args = argparse.Namespace(pdf="form.pdf", user="u1", pdf_doc_id="lp_v1", data=data_path)
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            result = _fill(args)
        assert result == 0
        call_kwargs = mock_mapper_orch.fill_pdf.call_args[1]
        assert call_kwargs["user_data"] == {"investor_name": "Jane"}

    def test_fill_with_inline_json(self, mock_mapper_orch):
        args = argparse.Namespace(
            pdf="form.pdf", user="u1", pdf_doc_id="lp_v1",
            data='{"investor_name": "Jane"}',
        )
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            result = _fill(args)
        assert result == 0

    def test_fill_with_invalid_json_raises(self, mock_mapper_orch):
        args = argparse.Namespace(
            pdf="form.pdf", user="u1", pdf_doc_id="lp_v1",
            data="not-a-file-and-not-json",
        )
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            with pytest.raises(json.JSONDecodeError):
                _fill(args)


class TestMapperRun:
    def test_no_subcommand_returns_1(self, mock_mapper_orch):
        args = argparse.Namespace(mapper_command=None)
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            result = mapper_run(args)
        assert result == 1

    def test_unknown_subcommand_returns_0(self, mock_mapper_orch):
        args = argparse.Namespace(mapper_command="nonexistent")
        fake_mod = _mock_mapper_module(mock_mapper_orch)
        with patch.dict(sys.modules, {"pdf_autofillr_mapper": fake_mod}):
            result = mapper_run(args)
        assert result == 0


# ── Doc Upload ────────────────────────────────────────────────────────────────

class TestDocUploadProcess:
    def test_process_calls_client(self, mock_doc_upload_client):
        args = argparse.Namespace(
            doc="investor.pdf", pdf="blank.pdf",
            schema_keys_path="configs/form_keys.json",
            user_id="u1", pdf_doc_id="lp_v1",
        )
        fake_mod = _mock_doc_module(mock_doc_upload_client)
        with patch.dict(sys.modules, {"pdf_autofillr_doc_upload": fake_mod}):
            result = _process(args)
        assert result == 0
        mock_doc_upload_client.process.assert_called_once_with(
            document_path="investor.pdf", pdf_path="blank.pdf",
            schema_keys_path="configs/form_keys.json",
            user_id="u1", pdf_doc_id="lp_v1",
        )


class TestDocUploadRun:
    def test_no_subcommand_returns_1(self, mock_doc_upload_client):
        args = argparse.Namespace(doc_command=None)
        fake_mod = _mock_doc_module(mock_doc_upload_client)
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
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _info(args)
        assert result == 0
        assert "email-validator" in capsys.readouterr().out

    def test_info_not_found(self):
        args = argparse.Namespace(name="nonexistent", category=None)
        mock_mgr = MagicMock()
        mock_mgr.get_plugin_info.return_value = None
        fake_mod = _mock_plugins_module(mock_mgr)
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = _info(args)
        assert result == 1


class TestPluginsRun:
    def test_no_subcommand_returns_1(self):
        args = argparse.Namespace(plugins_command=None)
        mock_mgr = MagicMock()
        mock_mgr.list_plugins.return_value = {}
        fake_mod = _mock_plugins_module(mock_mgr)
        with patch.dict(sys.modules, {"pdf_autofillr_plugins": fake_mod}):
            result = plugins_run(args)
        assert result == 1
