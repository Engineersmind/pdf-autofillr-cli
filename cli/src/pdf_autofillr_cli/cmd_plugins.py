"""
pdf-autofillr-cli plugins <command>

Inspect, list, and validate installed plugins.
"""

from __future__ import annotations

import argparse
import json


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "plugins",
        help="Plugin management commands",
        description="Inspect and validate pdf-autofillr plugins.",
    )
    sub = p.add_subparsers(dest="plugins_command", metavar="COMMAND")

    # ── list ──────────────────────────────────────────────────────────────
    ls = sub.add_parser("list", help="List all discovered plugins")
    ls.add_argument(
        "--path", default=None, help="Directory or module path to scan (default: installed plugins)"
    )
    ls.add_argument(
        "--category",
        default=None,
        help="Filter by category: extractor, mapper, validator, filler, …",
    )
    ls.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")

    # ── info ──────────────────────────────────────────────────────────────
    inf = sub.add_parser("info", help="Show detailed info for a single plugin")
    inf.add_argument("name", help="Plugin name")
    inf.add_argument("--category", default=None)

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module

    require_module("pdf_autofillr_plugins", "pip install pdf-autofillr-plugins")

    if not args.plugins_command:
        print("Usage: pdf-autofillr-cli plugins <command>")
        print("Commands: list, info")
        return 1

    if args.plugins_command == "list":
        return _list(args)
    elif args.plugins_command == "info":
        return _info(args)

    return 0


def _list(args: argparse.Namespace) -> int:
    from pdf_autofillr_plugins import PluginManager  # type: ignore

    paths = [args.path] if args.path else []
    manager = PluginManager(plugin_paths=paths if paths else None)

    if paths:
        manager.discover_plugins(paths)

    all_plugins = manager.list_plugins(category=args.category)

    if args.as_json:
        result: dict[str, list] = {}
        for cat, names in all_plugins.items():
            result[cat] = []
            for name in names:
                info = manager.get_plugin_info(name, cat)
                result[cat].append(info or {"name": name})
        print(json.dumps(result, indent=2))
        return 0

    if not all_plugins or all(len(v) == 0 for v in all_plugins.values()):
        print("\n  No plugins discovered.")
        if not paths:
            print("  Use --path to point to a directory containing plugins.\n")
        return 0

    print()
    for cat, names in all_plugins.items():
        if not names:
            continue
        print(f"  {cat.upper()}")
        print(f"  {'─' * 40}")
        for name in names:
            info = manager.get_plugin_info(name, cat)
            if info:
                print(f"    {info['name']:<30} v{info['version']}  {info['description']}")
            else:
                print(f"    {name}")
        print()

    return 0


def _info(args: argparse.Namespace) -> int:
    from pdf_autofillr_plugins import PluginManager  # type: ignore

    manager = PluginManager()
    info = manager.get_plugin_info(args.name, args.category)

    if not info:
        print(f"\n  Plugin '{args.name}' not found.")
        print("  Try: pdf-autofillr-cli plugins list\n")
        return 1

    print(json.dumps(info, indent=2))
    return 0
