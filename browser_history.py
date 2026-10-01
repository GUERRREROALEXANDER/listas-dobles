"""Browser history modeled with a doubly linked list."""

from linked_list import DoublyLinkedList, ListError


SAMPLE_PAGES = (
    "Home",
    "Search results",
    "Python docs",
    "Data structures",
)


class BrowserHistory:
    def __init__(self, pages: tuple[str, ...] = SAMPLE_PAGES) -> None:
        self.pages = DoublyLinkedList(list(pages))
        self.pages.cursor = self.pages.tail

    def visit(self, title: str) -> None:
        title = self.pages._check_value(title)
        if self.pages.cursor is not None:
            node = self.pages.cursor.next
            while node is not None:
                following = node.next
                node.previous = None
                node.next = None
                self.pages.size -= 1
                node = following
            self.pages.cursor.next = None
            self.pages.tail = self.pages.cursor
        self.pages.append(title)
        self.pages.cursor = self.pages.tail

    def back(self) -> str:
        return self.pages.move("previous")

    def forward(self) -> str:
        return self.pages.move("next")

    def select(self, index: int) -> str:
        return self.pages.select(index)

    def insert(self, index: int, title: str) -> None:
        self.pages.insert(index, title)

    def remove(self, index: int) -> str:
        return self.pages.remove(index)

    def reset(self) -> None:
        self.pages.clear()
        for title in SAMPLE_PAGES:
            self.pages.append(title)
        self.pages.cursor = self.pages.tail

    def clear(self) -> None:
        self.pages.clear()

    def snapshot(self) -> dict:
        return self.pages.snapshot()
