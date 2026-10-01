"""Doubly linked list with explicit node links and a movable cursor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


class ListError(ValueError):
    """An invalid index, value, or operation."""


@dataclass(slots=True)
class Node:
    value: str
    previous: Node | None = None
    next: Node | None = None


class DoublyLinkedList:
    def __init__(self, values: list[str] | None = None) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.cursor: Node | None = None
        self.size = 0
        for value in values or []:
            self.append(value)
        self.cursor = self.head

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[str]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __reversed__(self) -> Iterator[str]:
        node = self.tail
        while node is not None:
            yield node.value
            node = node.previous

    def _check_value(self, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ListError("Enter a value.")
        value = value.strip()
        if len(value) > 24:
            raise ListError("Use at most 24 characters.")
        return value

    def _node_at(self, index: int) -> Node:
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < self.size:
            raise ListError(f"Index must be between 0 and {self.size - 1}.")
        if index < self.size // 2:
            node = self.head
            for _ in range(index):
                node = node.next
        else:
            node = self.tail
            for _ in range(self.size - index - 1):
                node = node.previous
        return node

    def append(self, value: str) -> None:
        value = self._check_value(value)
        node = Node(value, previous=self.tail)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1
        if self.cursor is None:
            self.cursor = node

    def prepend(self, value: str) -> None:
        self.insert(0, value)

    def insert(self, index: int, value: str) -> None:
        value = self._check_value(value)
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index <= self.size:
            raise ListError(f"Insertion index must be between 0 and {self.size}.")
        if index == self.size:
            self.append(value)
            return
        after = self._node_at(index)
        before = after.previous
        node = Node(value, previous=before, next=after)
        after.previous = node
        if before is None:
            self.head = node
        else:
            before.next = node
        self.size += 1

    def remove(self, index: int) -> str:
        node = self._node_at(index)
        before, after = node.previous, node.next
        if before is None:
            self.head = after
        else:
            before.next = after
        if after is None:
            self.tail = before
        else:
            after.previous = before
        if self.cursor is node:
            self.cursor = after or before
        self.size -= 1
        node.previous = node.next = None
        return node.value

    def move(self, direction: str) -> str:
        if direction not in ("next", "previous"):
            raise ListError("Direction must be next or previous.")
        if self.cursor is None:
            raise ListError("The list is empty.")
        destination = self.cursor.next if direction == "next" else self.cursor.previous
        if destination is None:
            raise ListError("The cursor is already at the end.")
        self.cursor = destination
        return destination.value

    def select(self, index: int) -> str:
        self.cursor = self._node_at(index)
        return self.cursor.value

    def clear(self) -> None:
        self.head = self.tail = self.cursor = None
        self.size = 0

    def snapshot(self) -> dict:
        nodes = []
        current = self.head
        index = 0
        while current is not None:
            nodes.append({
                "index": index,
                "value": current.value,
                "previous": current.previous.value if current.previous else None,
                "next": current.next.value if current.next else None,
                "selected": current is self.cursor,
            })
            current = current.next
            index += 1
        return {
            "size": self.size,
            "head": self.head.value if self.head else None,
            "tail": self.tail.value if self.tail else None,
            "cursor": self.cursor.value if self.cursor else None,
            "nodes": nodes,
            "reverse": list(reversed(self)),
        }
