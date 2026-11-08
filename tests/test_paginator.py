"""Unit tests for mcp-stateful-cursor-paginator."""
import unittest
from mcp_stateful_cursor_paginator.paginator import MCPStatefulCursorPaginator


class TestMCPStatefulCursorPaginator(unittest.TestCase):
    def test_pagination_flow(self):
        p = MCPStatefulCursorPaginator(default_page_size=2)
        dataset = ["a", "b", "c", "d", "e"]

        p1 = p.paginate(dataset)
        self.assertEqual(p1.items, ["a", "b"])
        self.assertIsNotNone(p1.next_cursor)

        p2 = p.paginate(dataset, cursor=p1.next_cursor)
        self.assertEqual(p2.items, ["c", "d"])

        p3 = p.paginate(dataset, cursor=p2.next_cursor)
        self.assertEqual(p3.items, ["e"])
        self.assertIsNone(p3.next_cursor)
