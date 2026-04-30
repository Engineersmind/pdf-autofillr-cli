"""
Integration tests — parse real argv arrays through the full CLI parser.
No module imports are mocked; these test the argparse wiring end-to-end.
"""
import pytest
from pdf_autofillr_cli.main import build_parser


class TestFullParserIntegration:
    """Test that every subcommand parses its arguments correctly."""

    def setup_method(self):
        self.parser = build_parser()

    # ── status ───────────────────────────────────────────────────────────
    def test_status_default(self):
        args = self.parser.parse_args(["status"])
        assert args.command == "status"
        assert args.path == "."

    def test_status_custom_path(self):
        args = self.parser.parse_args(["status", "--path", "/tmp/myproject"])
        assert args.path == "/tmp/myproject"

    # ── setup ────────────────────────────────────────────────────────────
    def test_setup_defaults(self):
        args = self.parser.parse_args(["setup"])
        assert args.command == "setup"
        assert args.module == "all"
        assert args.force is False

    def test_setup_with_module_and_force(self):
        args = self.parser.parse_args(["setup", "--module", "rag", "--force"])
        assert args.module == "rag"
        assert args.force is True

    # ── rag ──────────────────────────────────────────────────────────────
    def test_rag_predict_parses(self):
        args = self.parser.parse_args([
            "rag", "predict",
            "--user", "u1", "--session", "s1", "--pdf", "p1",
            "--fields", "fields.json", "--hash", "abc123",
        ])
        assert args.rag_command == "predict"
        assert args.user == "u1"
        assert args.hash == "abc123"

    def test_rag_metrics_global(self):
        args = self.parser.parse_args(["rag", "metrics", "--type", "global"])
        assert args.rag_command == "metrics"
        assert args.metric_type == "global"

    def test_rag_feedback_parses(self):
        args = self.parser.parse_args([
            "rag", "feedback",
            "--user", "u1", "--session", "s1", "--pdf", "p1",
            "--errors", "errors.json",
        ])
        assert args.rag_command == "feedback"
        assert args.errors == "errors.json"

    def test_rag_system_info(self):
        args = self.parser.parse_args(["rag", "system-info"])
        assert args.rag_command == "system-info"

    def test_rag_init_vectors_with_flags(self):
        args = self.parser.parse_args([
            "rag", "init-vectors",
            "--backend", "openai", "--force", "--batch-size", "25",
        ])
        assert args.rag_command == "init-vectors"
        assert args.backend == "openai"
        assert args.force is True
        assert args.batch_size == 25

    def test_rag_error_analytics(self):
        args = self.parser.parse_args([
            "rag", "error-analytics", "--from", "2026-01-01T00:00:00Z",
        ])
        assert args.rag_command == "error-analytics"
        assert args.date_from == "2026-01-01T00:00:00Z"

    # ── mapper ───────────────────────────────────────────────────────────
    def test_mapper_embed_parses(self):
        args = self.parser.parse_args([
            "mapper", "embed",
            "--pdf", "blank.pdf", "--user", "u1", "--id", "lp_v1",
        ])
        assert args.mapper_command == "embed"
        assert args.pdf_doc_id == "lp_v1"

    def test_mapper_fill_parses(self):
        args = self.parser.parse_args([
            "mapper", "fill",
            "--pdf", "blank.pdf", "--user", "u1", "--id", "lp_v1",
            "--data", "data.json",
        ])
        assert args.mapper_command == "fill"
        assert args.data == "data.json"

    # ── doc-upload ───────────────────────────────────────────────────────
    def test_doc_upload_process_parses(self):
        args = self.parser.parse_args([
            "doc-upload", "process",
            "--doc", "investor.pdf",
            "--pdf", "blank.pdf",
            "--schema", "form_keys.json",
            "--user", "u1",
            "--id", "lp_v1",
        ])
        assert args.doc_command == "process"
        assert args.doc == "investor.pdf"
        assert args.user_id == "u1"

    # ── chatbot ──────────────────────────────────────────────────────────
    def test_chatbot_start_parses(self):
        args = self.parser.parse_args(["chatbot", "start", "--port", "9000"])
        assert args.chatbot_command == "start"
        assert args.port == 9000

    def test_chatbot_session_parses(self):
        args = self.parser.parse_args([
            "chatbot", "session", "--pdf", "blank.pdf", "--user", "u1",
        ])
        assert args.chatbot_command == "session"
        assert args.pdf == "blank.pdf"
        assert args.session is None  # optional

    # ── plugins ──────────────────────────────────────────────────────────
    def test_plugins_list_parses(self):
        args = self.parser.parse_args(["plugins", "list"])
        assert args.plugins_command == "list"
        assert args.as_json is False

    def test_plugins_list_json_flag(self):
        args = self.parser.parse_args(["plugins", "list", "--json"])
        assert args.as_json is True

    def test_plugins_list_category_filter(self):
        args = self.parser.parse_args(["plugins", "list", "--category", "validator"])
        assert args.category == "validator"

    def test_plugins_info_parses(self):
        args = self.parser.parse_args(["plugins", "info", "email-validator"])
        assert args.plugins_command == "info"
        assert args.name == "email-validator"

    # ── invalid ──────────────────────────────────────────────────────────
    def test_invalid_command_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["nonexistent-command"])

    def test_rag_invalid_metric_type_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["rag", "metrics", "--type", "invalid"])
