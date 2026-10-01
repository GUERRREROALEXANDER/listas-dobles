"""Behavior checks for pointer integrity and cursor movement."""

import unittest

from linked_list import DoublyLinkedList, ListError


class DoublyLinkedListTests(unittest.TestCase):
    def assert_links(self, structure: DoublyLinkedList, expected: list[str]) -> None:
        self.assertEqual(list(structure), expected)
        self.assertEqual(list(reversed(structure)), expected[::-1])
        self.assertEqual(len(structure), len(expected))
        self.assertEqual(structure.head.value if structure.head else None, expected[0] if expected else None)
        self.assertEqual(structure.tail.value if structure.tail else None, expected[-1] if expected else None)
        node = structure.head
        previous = None
        for value in expected:
            self.assertEqual(node.value, value)
            self.assertIs(node.previous, previous)
            previous, node = node, node.next
        self.assertIsNone(node)

    def test_insert_and_remove_at_both_ends_and_middle(self) -> None:
        structure = DoublyLinkedList(["B", "D"])
        structure.prepend("A")
        structure.insert(2, "C")
        structure.append("E")
        self.assert_links(structure, ["A", "B", "C", "D", "E"])
        self.assertEqual(structure.remove(2), "C")
        self.assertEqual(structure.remove(0), "A")
        self.assertEqual(structure.remove(2), "E")
        self.assert_links(structure, ["B", "D"])

    def test_cursor_follows_actual_links_and_survives_removal(self) -> None:
        structure = DoublyLinkedList(["A", "B", "C"])
        self.assertEqual(structure.move("next"), "B")
        self.assertEqual(structure.move("previous"), "A")
        structure.select(1)
        self.assertEqual(structure.remove(1), "B")
        self.assertEqual(structure.cursor.value, "C")
        self.assertEqual(structure.move("previous"), "A")
        with self.assertRaises(ListError):
            structure.move("previous")

    def test_empty_list_and_validation(self) -> None:
        structure = DoublyLinkedList()
        self.assert_links(structure, [])
        with self.assertRaises(ListError):
            structure.move("next")
        with self.assertRaises(ListError):
            structure.insert(1, "X")
        with self.assertRaises(ListError):
            structure.append("   ")
        with self.assertRaises(ListError):
            structure.insert(True, "X")
        structure.append("Only")
        self.assertEqual(structure.remove(0), "Only")
        self.assert_links(structure, [])
        self.assertIsNone(structure.cursor)

    def test_snapshot_shows_neighbors_in_both_directions(self) -> None:
        structure = DoublyLinkedList(["A", "B", "C"])
        structure.select(1)
        state = structure.snapshot()
        self.assertEqual(state["reverse"], ["C", "B", "A"])
        self.assertEqual(state["nodes"][1], {
            "index": 1, "value": "B", "previous": "A", "next": "C", "selected": True,
        })


if __name__ == "__main__":
    unittest.main()
