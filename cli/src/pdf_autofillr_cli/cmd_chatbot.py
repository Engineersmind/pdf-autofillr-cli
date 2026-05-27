"""
pdf-autofillr-cli chatbot <command>

Commands to start and interact with the chatbot module.
"""

from __future__ import annotations

import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "chatbot",
        help="Chatbot session commands",
        description="Conversational PDF form-filling chatbot.",
    )
    sub = p.add_subparsers(dest="chatbot_command", metavar="COMMAND")

    # ── start (API server) ────────────────────────────────────────────────
    srv = sub.add_parser("start", help="Start the chatbot API server")
    srv.add_argument("--host", default="0.0.0.0")
    srv.add_argument("--port", default=8000, type=int)
    srv.add_argument("--reload", action="store_true", help="Auto-reload on code change")

    # ── session ───────────────────────────────────────────────────────────
    ses = sub.add_parser("session", help="Start an interactive chatbot session (CLI mode)")
    ses.add_argument("--pdf", required=True, help="Path to blank PDF form")
    ses.add_argument("--user", required=True, help="User ID")
    ses.add_argument("--session", default=None, help="Resume existing session ID")

    # ── sessions ──────────────────────────────────────────────────────────
    sub.add_parser("sessions", help="List all active sessions")

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module

    require_module("chatbot", "pip install pdf-autofillr-chatbot")

    if not args.chatbot_command:
        print("Usage: pdf-autofillr-cli chatbot <command>")
        print("Commands: start, session, sessions")
        return 1

    if args.chatbot_command == "start":
        return _start_server(args)
    elif args.chatbot_command == "session":
        return _run_session(args)
    elif args.chatbot_command == "sessions":
        return _list_sessions()

    return 0


def _start_server(args: argparse.Namespace) -> int:
    try:
        import uvicorn
        from chatbot.entrypoints.fastapi_app import app

        print(f"\n  Starting chatbot server on http://{args.host}:{args.port}")
        print("  Swagger docs: http://localhost:{args.port}/docs\n")
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
    except ImportError:
        print("  uvicorn not installed. Run: pip install uvicorn")
        return 1
    return 0


def _run_session(args: argparse.Namespace) -> int:
    import uuid

    from chatbot import chatbotClient  # type: ignore
    from chatbot.config.form_config import FormConfig
    from chatbot.storage.local_storage import LocalStorage

    storage = LocalStorage(data_path="./data", config_path="./configs")
    form_config = FormConfig.from_directory("./configs")
    client = chatbotClient(storage=storage, form_config=form_config)

    session_id = args.session or str(uuid.uuid4())
    print(f"\n  Session: {session_id}")
    print(f"  PDF: {args.pdf}")
    print("  Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Session ended.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("  Bot: Goodbye!")
            break

        response, complete, data = client.send_message(
            user_id=args.user,
            session_id=session_id,
            message=user_input,
        )
        print(f"  Bot: {response}")

        if complete:
            print("\n  ✅  Form complete.\n")
            break

    return 0


def _list_sessions() -> int:
    try:
        # list_user_sessions requires a user_id — show all session files instead
        import pathlib

        session_dir = pathlib.Path("./data")
        if not session_dir.exists():
            print("  No sessions found (data/ directory does not exist).")
            return 0
        sessions = list(session_dir.rglob("*.json"))
        if not sessions:
            print("  No active sessions.")
        else:
            print(f"\n  Found {len(sessions)} session file(s):")
            for s in sessions:
                print(f"    {s}")
    except Exception as e:
        print(f"  Could not list sessions: {e}")
    return 0
