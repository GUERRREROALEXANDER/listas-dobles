"""Checks for browser history behavior and pointer integrity."""

import unittest

from browser_history import BrowserHistory, SAMPLE_PAGES
from linked_list import ListError


class BrowserHistoryTests(unittest.TestCase):
    def assert_links(self, history: BrowserHistory, expected: list[str]) -> None:
        self.assertEqual(list(history.pages), expected)
        self.assertEqual(list(reversed(history.pages)), expected[::-1])
        self.assertEqual(len(history.pages), len(expected))
        previous = None
        node = history.pages.head
        for value in expected:
            self.assertIsNotNone(node)
            self.assertEqual(node.value, value)
            self.assertIs(node.previous, previous)
            previous, node = node, node.next
        self.assertIsNone(node)
        self.assertIs(history.pages.tail, previous)

    def test_back_and_forward_follow_node_links(self) -> None:
        history = BrowserHistory(("A", "B", "C"))
        self.assertEqual(history.back(), "B")
        self.assertEqual(history.back(), "A")
        self.assertEqual(history.forward(), "B")
        self.assertEqual(history.snapshot()["cursor"], "B")
        with self.assertRaises(ListError):
            history.back()
            history.back()

    def test_new_visit_discards_forward_branch(self) -> None:
        history = BrowserHistory(("A", "B", "C", "D"))
        history.back()
        history.back()
        history.visit("E")
        self.assert_links(history, ["A", "B", "E"])
        self.assertEqual(history.snapshot()["cursor"], "E")
        with self.assertRaises(ListError):
            history.forward()

    def test_visit_on_empty_history(self) -> None:
        history = BrowserHistory(())
        history.visit("First")
        self.assert_links(history, ["First"])
        self.assertEqual(history.snapshot()["cursor"], "First")

    def test_insert_remove_and_reset(self) -> None:
        history = BrowserHistory(("A", "C"))
        history.insert(1, "B")
        self.assert_links(history, ["A", "B", "C"])
        history.select(1)
        self.assertEqual(history.remove(1), "B")
        self.assert_links(history, ["A", "C"])
        self.assertEqual(history.snapshot()["cursor"], "C")
        history.clear()
        self.assert_links(history, [])
        history.reset()
        self.assert_links(history, list(SAMPLE_PAGES))
        self.assertEqual(history.snapshot()["cursor"], SAMPLE_PAGES[-1])

    def test_invalid_input_does_not_change_history(self) -> None:
        history = BrowserHistory(("A", "B"))
        for title in ("", "   ", "X" * 25):
            with self.assertRaises(ListError):
                history.visit(title)
        with self.assertRaises(ListError):
            history.insert(-1, "C")
        with self.assertRaises(ListError):
            history.remove(5)
        self.assert_links(history, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
