# Linked List Lab

An interactive doubly linked list built entirely in Python. The data structure uses nodes with explicit `previous` and `next` references. The desktop interface is made with Tkinter. No packages, browser, Node.js, or JavaScript are needed.

## Run

From PowerShell:

```powershell
cd "D:\Escritorio\listas dobles"
python gui.py
```

If `python` is unavailable on the command line, use the installed Python executable or `uv run --no-project --python 3.13 gui.py`.

## Use the app

- Enter a value and add it to the head or tail.
- Enter a zero-based position to insert or remove a node.
- Click a node to select it, then use Previous and Next to move the cursor through the actual links.
- Switch to "Show tail to head" to inspect the chain backward.
- Reset Example restores the five sample nodes. Clear List removes all nodes.

Each card displays the node's index, value, previous neighbor, and next neighbor. The selected node appears in the inspector. The summary displays the head, tail, and total count. Invalid positions and empty values show an English error message at the bottom.

## Files

- `linked_list.py`: Node, DoublyLinkedList, cursor operations, and validation.
- `gui.py`: Tkinter controls, canvas visualization, and interaction.
- `test_linked_list.py`: pointer, cursor, boundary, and snapshot checks.

## Tests

```powershell
python -m unittest discover -v
```

## Reference

The repository at https://github.com/nik129linux/Taller-Listas-Dobles was studied for its explanation of forward and backward links, insertion, deletion, and traversal. This project has its own Python implementation, desktop interface, sample data, and visual design.
# listas-dobles
