"""Unit tests for pdf-autofillr-cli rag commands."""

import argparse
import json
import sys
from unittest.mock import MagicMock, patch

import pytest

from pdf_autofillr_cli.cmd_rag import (
    _error_analytics,
    _feedback,
    _load_category,
    _metrics,
    _predict,
)


def _fake_ragpdf(mock_client):
    mod = MagicMock()
    mod.RAGPDFClient = MagicMock()
    mod.RAGPDFClient.from_env.return_value = mock_client
    return mod


class TestLoadCategory:
    def test_empty_string(self):
        assert _load_category("") == {}

    def test_empty_json(self):
        assert _load_category("{}") == {}

    def test_inline_json(self):
        assert _load_category('{"category":"Finance"}') == {"category": "Finance"}

    def test_file_path(self, tmp_path):
        f = tmp_path / "cat.json"
        f.write_text('{"category":"PM"}')
        assert _load_category(str(f)) == {"category": "PM"}

    def test_invalid_json_raises(self):
        with pytest.raises(json.JSONDecodeError):
            _load_category("bad-json")


class TestRagPredict:
    def test_predict_calls_client(self, tmp_json, mock_rag_client):
        fp = tmp_json("f.json", [{"field_id": "f1"}])
        cp = tmp_json("c.json", {"category": "Finance"})
        args = argparse.Namespace(
            user="u1", session="s1", pdf="p1", fields=fp, hash="abc", category=cp
        )
        _predict(args, mock_rag_client)
        mock_rag_client.get_predictions.assert_called_once()

    def test_unwraps_wrapped_fields(self, tmp_json, mock_rag_client):
        fp = tmp_json("f.json", {"fields": [{"field_id": "f1"}]})
        args = argparse.Namespace(
            user="u1", session="s1", pdf="p1", fields=fp, hash="abc", category="{}"
        )
        _predict(args, mock_rag_client)
        assert isinstance(mock_rag_client.get_predictions.call_args[0][3], list)


class TestRagFeedback:
    def test_feedback_calls_client(self, tmp_json, mock_rag_client):
        ep = tmp_json("e.json", [{"error_type": "x"}])
        args = argparse.Namespace(user="u1", session="s1", pdf="p1", errors=ep)
        _feedback(args, mock_rag_client)
        mock_rag_client.submit_feedback.assert_called_once_with(
            "u1", "s1", "p1", [{"error_type": "x"}]
        )

    def test_unwraps_wrapped_errors(self, tmp_json, mock_rag_client):
        ep = tmp_json("e.json", {"errors": [{"error_type": "x"}]})
        args = argparse.Namespace(user="u1", session="s1", pdf="p1", errors=ep)
        _feedback(args, mock_rag_client)
        assert isinstance(mock_rag_client.submit_feedback.call_args[0][3], list)


class TestRagMetrics:
    def test_metrics_global(self, mock_rag_client):
        args = argparse.Namespace(
            func=None,
            command="rag",
            rag_command="metrics",
            metric_type="global",
            user=None,
            session=None,
            pdf=None,
            category=None,
            subcategory=None,
            doctype=None,
            pdf_hash=None,
        )
        _metrics(args, mock_rag_client)
        mock_rag_client.get_metrics.assert_called_with("global")

    def test_metrics_per_pdf(self, mock_rag_client):
        args = argparse.Namespace(
            func=None,
            command="rag",
            rag_command="metrics",
            metric_type="pdf",
            user="u1",
            session="s1",
            pdf="p1",
            category=None,
            subcategory=None,
            doctype=None,
            pdf_hash=None,
        )
        _metrics(args, mock_rag_client)
        assert mock_rag_client.get_metrics.call_args[0][0] == "pdf"


class TestRagErrorAnalytics:
    def test_error_analytics(self, mock_rag_client):
        args = argparse.Namespace(date_from="2026-01-01Z", date_to=None, category=None)
        _error_analytics(args, mock_rag_client)
        mock_rag_client.get_error_analytics.assert_called_once()


class TestRagRun:
    def test_no_subcommand_returns_1(self, mock_rag_client):
        from pdf_autofillr_cli.cmd_rag import run

        args = argparse.Namespace(rag_command=None)
        with patch.dict(sys.modules, {"ragpdf": _fake_ragpdf(mock_rag_client)}):
            result = run(args)
        assert result == 1

    def test_system_info(self, mock_rag_client):
        from pdf_autofillr_cli.cmd_rag import run

        args = argparse.Namespace(rag_command="system-info")
        with patch.dict(sys.modules, {"ragpdf": _fake_ragpdf(mock_rag_client)}):
            result = run(args)
        assert result == 0
        mock_rag_client.get_system_info.assert_called_once()
