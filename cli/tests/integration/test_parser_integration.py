"""
Integration tests — parse real argv arrays through the full CLI parser.
No module imports are mocked; these test the argparse wiring end-to-end.
"""

import pytest

from pdf_autofillr_cli.main import build_parser


class TestFullParserIntegration:

    def setup_method(self):
        self.parser = build_parser()

    # ── extract ───────────────────────────────────────────────────────────
    def test_extract_required_args(self):
        args = self.parser.parse_args(["extract", "form.pdf"])
        assert args.command == "extract"
        assert args.pdf == "form.pdf"
        assert args.output is None
        assert args.pretty is False

    def test_extract_with_output(self):
        args = self.parser.parse_args(["extract", "form.pdf", "--output", "schema.json"])
        assert args.output == "schema.json"

    def test_extract_with_pretty(self):
        args = self.parser.parse_args(["extract", "form.pdf", "--pretty"])
        assert args.pretty is True

    def test_extract_short_output_flag(self):
        args = self.parser.parse_args(["extract", "form.pdf", "-o", "out.json"])
        assert args.output == "out.json"

    # ── embed ─────────────────────────────────────────────────────────────
    def test_embed_required_args(self):
        args = self.parser.parse_args(["embed", "form.pdf", "--schema", "configs/form_keys.json"])
        assert args.command == "embed"
        assert args.pdf == "form.pdf"
        assert args.schema == "configs/form_keys.json"

    def test_embed_with_output(self):
        args = self.parser.parse_args(
            ["embed", "form.pdf", "--schema", "configs/form_keys.json", "--output", "out.pdf"]
        )
        assert args.output == "out.pdf"

    def test_embed_with_user_and_id(self):
        args = self.parser.parse_args(["embed", "form.pdf", "--schema", "configs/form_keys.json"])
        assert args.pdf == "form.pdf"

    def test_embed_missing_schema_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["embed", "form.pdf"])

    # ── fill ──────────────────────────────────────────────────────────────
    def test_fill_required_args(self):
        args = self.parser.parse_args(["fill", "form.pdf", "--data", "data.json"])
        assert args.command == "fill"
        assert args.pdf == "form.pdf"
        assert args.data == "data.json"

    def test_fill_with_output(self):
        args = self.parser.parse_args(
            ["fill", "form.pdf", "--data", "data.json", "--output", "filled.pdf"]
        )
        assert args.output == "filled.pdf"

    def test_fill_missing_data_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["fill", "form.pdf"])

    # ── validate ──────────────────────────────────────────────────────────
    def test_validate_required_args(self):
        args = self.parser.parse_args(["validate", "filled.pdf", "--schema", "schema.json"])
        assert args.command == "validate"
        assert args.pdf == "filled.pdf"
        assert args.schema == "schema.json"
        assert args.strict is False

    def test_validate_strict_flag(self):
        args = self.parser.parse_args(
            ["validate", "filled.pdf", "--schema", "schema.json", "--strict"]
        )
        assert args.strict is True

    def test_validate_missing_schema_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["validate", "filled.pdf"])

    def test_validate_short_schema_flag(self):
        args = self.parser.parse_args(["validate", "filled.pdf", "-s", "schema.json"])
        assert args.schema == "schema.json"

    # ── run ───────────────────────────────────────────────────────────────
    def test_run_required_args(self):
        args = self.parser.parse_args(
            ["run", "form.pdf", "--schema", "configs/form_keys.json", "--data", "data.json"]
        )
        assert args.command == "run"
        assert args.pdf == "form.pdf"
        assert args.data == "data.json"

    def test_run_with_output(self):
        args = self.parser.parse_args(
            [
                "run",
                "form.pdf",
                "--schema",
                "configs/form_keys.json",
                "--data",
                "data.json",
                "--output",
                "out.pdf",
            ]
        )
        assert args.output == "out.pdf"

    # ── batch ─────────────────────────────────────────────────────────────
    def test_batch_required_args(self):
        args = self.parser.parse_args(
            [
                "batch",
                "--template",
                "form.pdf",
                "--schema",
                "configs/form_keys.json",
                "--input",
                "data/",
                "--output",
                "output/",
            ]
        )
        assert args.command == "batch"
        assert args.template == "form.pdf"
        assert args.input == "data/"
        assert args.output == "output/"

    def test_batch_missing_template_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(
                [
                    "batch",
                    "--schema",
                    "configs/form_keys.json",
                    "--input",
                    "data/",
                    "--output",
                    "output/",
                ]
            )

    # ── status ────────────────────────────────────────────────────────────
    def test_status_parses(self):
        args = self.parser.parse_args(["status"])
        assert args.command == "status"

    # ── setup ─────────────────────────────────────────────────────────────
    def test_setup_parses(self):
        args = self.parser.parse_args(["setup"])
        assert args.command == "setup"

    # ── chatbot ───────────────────────────────────────────────────────────
    def test_chatbot_session_parses(self):
        args = self.parser.parse_args(["chatbot", "session", "--pdf", "form.pdf", "--user", "u1"])
        assert args.chatbot_command == "session"
        assert args.pdf == "form.pdf"
        assert args.session is None

    def test_chatbot_start_parses(self):
        args = self.parser.parse_args(["chatbot", "start", "--port", "9000"])
        assert args.chatbot_command == "start"
        assert args.port == 9000

    # ── doc-upload ────────────────────────────────────────────────────────
    def test_doc_upload_process_parses(self):
        args = self.parser.parse_args(
            [
                "doc-upload",
                "process",
                "--doc",
                "investor.pdf",
                "--pdf",
                "blank.pdf",
                "--schema",
                "form_keys.json",
                "--user",
                "u1",
                "--id",
                "lp_v1",
            ]
        )
        assert args.doc_command == "process"
        assert args.doc == "investor.pdf"
        assert args.user_id == "u1"

    # ── mapper ────────────────────────────────────────────────────────────
    def test_mapper_embed_parses(self):
        args = self.parser.parse_args(
            ["mapper", "embed", "--pdf", "form.pdf", "--schema", "configs/form_keys.json"]
        )
        assert args.mapper_command == "embed"
        assert args.pdf == "form.pdf"

    def test_mapper_fill_parses(self):
        args = self.parser.parse_args(
            ["mapper", "fill", "--pdf", "form.pdf", "--data", "data.json"]
        )
        assert args.mapper_command == "fill"
        assert args.data == "data.json"

    # ── rag ───────────────────────────────────────────────────────────────
    def test_rag_predict_parses(self):
        args = self.parser.parse_args(
            [
                "rag",
                "predict",
                "--user",
                "u1",
                "--session",
                "s1",
                "--pdf",
                "p1",
                "--fields",
                "fields.json",
                "--hash",
                "abc123",
            ]
        )
        assert args.rag_command == "predict"
        assert args.hash == "abc123"

    def test_rag_system_info_parses(self):
        args = self.parser.parse_args(["rag", "system-info"])
        assert args.rag_command == "system-info"

    def test_rag_metrics_parses(self):
        args = self.parser.parse_args(["rag", "metrics", "--type", "global"])
        assert args.rag_command == "metrics"
        assert args.metric_type == "global"

    # ── plugins ───────────────────────────────────────────────────────────
    def test_plugins_list_parses(self):
        args = self.parser.parse_args(["plugins", "list"])
        assert args.plugins_command == "list"
        assert args.as_json is False

    def test_plugins_list_json_flag(self):
        args = self.parser.parse_args(["plugins", "list", "--json"])
        assert args.as_json is True

    def test_plugins_info_parses(self):
        args = self.parser.parse_args(["plugins", "info", "my-plugin"])
        assert args.plugins_command == "info"
        assert args.name == "my-plugin"

    # ── invalid ───────────────────────────────────────────────────────────
    def test_invalid_command_exits(self):
        with pytest.raises(SystemExit):
            self.parser.parse_args(["nonexistent-command"])
