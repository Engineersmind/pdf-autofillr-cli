"""Shared fixtures for CLI tests."""
import pytest
# from unittest.mock import MagicMock, patch
from unittest.mock import MagicMock

@pytest.fixture
def mock_rag_client():
    client = MagicMock()
    client.get_system_info.return_value = {"total_vectors": 12, "total_pdfs": 3}
    client.get_predictions.return_value = {"summary": {"total_fields": 2}, "predictions": {}}
    client.submit_feedback.return_value = {"corrected_fields": []}
    client.get_metrics.return_value = {"global": {"accuracy": 0.95}}
    client.get_error_analytics.return_value = {"total_errors": 0}
    return client


@pytest.fixture
def mock_mapper_orch():
    orch = MagicMock()
    orch.make_embed_file.return_value = MagicMock(embedded_pdf_path="/tmp/embedded.pdf")
    orch.fill_pdf.return_value = MagicMock(filled_pdf_path="/tmp/filled.pdf")
    return orch


@pytest.fixture
def mock_doc_upload_client():
    client = MagicMock()
    client.process.return_value = MagicMock(
        extracted_fields={"name": "Jane"},
        avg_confidence=0.92,
        filled_pdf_path="/tmp/filled.pdf",
    )
    return client


@pytest.fixture
def tmp_json(tmp_path):
    """Helper: write a JSON file and return its path."""
    def _write(name: str, data) -> str:
        import json
        p = tmp_path / name
        p.write_text(json.dumps(data))
        return str(p)
    return _write
