"""Core MCP Stateful Cursor Paginator implementation."""
import base64
import json
from typing import List, Dict, Any, Optional


class PageResult:
    def __init__(self, items: List[Any], next_cursor: Optional[str], total_count: int):
        self.items = items
        self.next_cursor = next_cursor
        self.total_count = total_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": self.items,
            "nextCursor": self.next_cursor,
            "totalCount": self.total_count,
            "hasMore": self.next_cursor is not None
        }


class MCPStatefulCursorPaginator:
    def __init__(self, default_page_size: int = 10):
        self.default_page_size = default_page_size

    def encode_cursor(self, offset: int) -> str:
        data = json.dumps({"offset": offset})
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def decode_cursor(self, cursor: str) -> int:
        try:
            raw = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
            data = json.loads(raw)
            return int(data.get("offset", 0))
        except Exception:
            return 0

    def paginate(self, dataset: List[Any], cursor: Optional[str] = None, page_size: Optional[int] = None) -> PageResult:
        limit = page_size if page_size is not None else self.default_page_size
        offset = self.decode_cursor(cursor) if cursor else 0

        items = dataset[offset:offset + limit]
        next_offset = offset + len(items)

        next_cursor = self.encode_cursor(next_offset) if next_offset < len(dataset) else None
        return PageResult(items, next_cursor, len(dataset))
