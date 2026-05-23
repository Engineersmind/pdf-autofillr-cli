"""Unit tests for pdf_autofillr_cli.utils."""
# import sys
import pytest
from unittest.mock import patch

from pdf_autofillr_cli.utils import (
    chatbot_available,
    rag_available,
    mapper_available,
    doc_upload_available,
    plugins_available,
    require_module,
)


class TestModuleAvailability:
    def test_available_returns_true_for_installed(self):
        # 'json' is always available - use it as a stand-in
        from pdf_autofillr_cli.utils import _try_import
        ok, ver, err = _try_import("json")
        assert ok is True
        assert err == ""

    def test_unavailable_returns_false_for_missing(self):
        from pdf_autofillr_cli.utils import _try_import
        ok, ver, err = _try_import("this_module_does_not_exist_xyz")
        assert ok is False
        assert err != ""

    def test_chatbot_available_returns_tuple(self):
        result = chatbot_available()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_rag_available_returns_tuple(self):
        result = rag_available()
        assert isinstance(result, tuple)

    def test_mapper_available_returns_tuple(self):
        result = mapper_available()
        assert isinstance(result, tuple)

    def test_doc_upload_available_returns_tuple(self):
        result = doc_upload_available()
        assert isinstance(result, tuple)

    def test_plugins_available_returns_tuple(self):
        result = plugins_available()
        assert isinstance(result, tuple)


class TestRequireModule:
    def test_require_exits_when_missing(self):
        with pytest.raises(SystemExit) as exc:
            require_module("this_does_not_exist_xyz", "pip install something")
        assert exc.value.code == 1

    def test_require_passes_when_installed(self):
        # Should not raise - json is always present
        require_module("json", "pip install json")
