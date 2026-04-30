"""
pdf-autofillr chatbot <command>

Commands to start and interact with the chatbot module.
"""
from __future__ import annotations

import argparse
import json


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
    ses.add_argument("--pdf",     required=True, help="Path to blank PDF form")
    ses.add_argument("--user",    required=True, help="User ID")
    ses.add_argument("--session", default=None,  help="Resume existing session ID")

    # ── sessions ──────────────────────────────────────────────────────────
    sub.add_parser("sessions", help="List all active sessions")

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module
    require_module("chatbot", "pip install pdf-autofillr-chatbot")

    if not args.chatbot_command:
        print("Usage: pdf-autofillr chatbot <command>")
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
    from chatbot import chatbotClient  # type: ignore

    client = chatbotClient.from_env()
    session = client.create_session(
        pdf_path=args.pdf,
        user_id=args.user,
        session_id=args.session,
    )
    print(f"\n  Session: {session.session_id}")
    print(f"  Bot: {session.greeting}\n")

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

        response = client.send_message(session.session_id, user_input)
        print(f"  Bot: {response.message}")

        if response.pdf_filled:
            print(f"\n  ✅  PDF filled: {response.filled_pdf_path}\n")
            break

    return 0


def _list_sessions() -> int:
    from chatbot import chatbotClient  # type: ignore
    client = chatbotClient.from_env()
    try:
        sessions = client.list_sessions()
        if not sessions:
            print("  No active sessions.")
        else:
            print(json.dumps(sessions, indent=2))
    except AttributeError:
        print("  list_sessions() not supported in this chatbot version.")
    return 0
