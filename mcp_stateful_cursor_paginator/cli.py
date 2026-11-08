"""CLI for mcp-stateful-cursor-paginator."""
import sys
import argparse
from .paginator import MCPStatefulCursorPaginator


def main():
    parser = argparse.ArgumentParser(description="MCP Stateful Cursor Paginator CLI")
    parser.add_argument("--demo", action="store_true", help="Run cursor paginator demo")
    args = parser.parse_args()

    if args.demo:
        paginator = MCPStatefulCursorPaginator(default_page_size=3)
        data = [f"Record_{i}" for i in range(1, 10)]

        p1 = paginator.paginate(data)
        print(f"[+] Page 1: {p1.items} | nextCursor={p1.next_cursor}")

        p2 = paginator.paginate(data, cursor=p1.next_cursor)
        print(f"[+] Page 2: {p2.items} | nextCursor={p2.next_cursor}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
