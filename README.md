# History Studio

An interactive browser history built entirely in Python. Every page is a node in a doubly linked list, with explicit `previous` and `next` references. The desktop interface uses Tkinter. No web frontend, Node.js, or extra packages are required.

This is a different scenario from the metro example in the reference repository. Browser Back follows `previous`, Forward follows `next`, and visiting a new page after going Back removes the old forward branch.

## Run

Double-click `open_app.pyw` in File Explorer, or run it from PowerShell:

```powershell
cd "D:\Escritorio\listas dobles"
& "C:\Users\Diego Guerrero\AppData\Local\Programs\Python\Python313\python.exe" gui.py
```

If Python is on your PATH, `python gui.py` also works.

## Use

- Enter a page title and choose **Visit page**.
- Choose **Back** or **Forward** to follow the actual links. Alt+Left and Alt+Right work too.
- Click a node or select a table row to make it the current page.
- Enter a zero-based position and a title to **Insert page at position**.
- Enter a position to **Remove page at position**.
- Switch **View from tail** to display the nodes in reverse order.
- **Restore example** loads four sample pages; **Clear history** starts over.

The diagram shows both directions between nodes. The table exposes the index and the two neighbors for each page. The pointer inspector shows the selected node's previous and next pages.

## Structure

- `linked_list.py`: `Node`, `DoublyLinkedList`, link updates, traversal, and validation.
- `browser_history.py`: browser Back, Forward, Visit, and the forward-branch rule.
- `gui.py`: Tkinter interface and visualization.
- `test_linked_list.py` and `test_browser_history.py`: checks of links, boundaries, cursor moves, and browser behavior.

## Tests

```powershell
& "C:\Users\Diego Guerrero\AppData\Local\Programs\Python\Python313\python.exe" -m unittest discover -v
```

## Reference

The repository at https://github.com/nik129linux/Taller-Listas-Dobles was reviewed for the doubly linked list concept. The application scenario, Python code, page data, and desktop interface here are original to History Studio.
