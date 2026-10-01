"""Tkinter desktop interface for a browser history backed by a doubly linked list."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from browser_history import BrowserHistory
from linked_list import ListError


class HistoryApp(tk.Tk):
    BG = "#F4F6FB"
    SURFACE = "#FFFFFF"
    NAVY = "#18243B"
    MUTED = "#536079"
    BLUE = "#315BB8"
    BLUE_DARK = "#244898"
    PALE = "#EAF0FE"
    BORDER = "#D8E0EE"
    ORANGE = "#DB6B33"
    ERROR = "#B43D48"

    def __init__(self) -> None:
        super().__init__()
        self.title("History Studio — Doubly Linked Lists")
        self.geometry("1240x820")
        self.minsize(980, 680)
        self.configure(bg=self.BG)

        self.history = BrowserHistory()
        self.title_input = tk.StringVar()
        self.index_input = tk.StringVar()
        self.message = tk.StringVar(value="Explore the history. Click a node or choose a row.")
        self.reverse = tk.BooleanVar(value=False)
        self._updating_table = False

        self._build()
        self._refresh()
        self.bind("<Alt-Left>", lambda _: self._action(self.history.back, "Moved back through previous."))
        self.bind("<Alt-Right>", lambda _: self._action(self.history.forward, "Moved forward through next."))

    def _label(self, parent: tk.Widget, text: str, size: int = 11,
               bold: bool = False, color: str | None = None,
               background: str | None = None) -> tk.Label:
        return tk.Label(parent, text=text, font=("Segoe UI", size, "bold" if bold else "normal"),
                        fg=color or self.NAVY, bg=background or self.SURFACE, anchor="w")

    def _button(self, parent: tk.Widget, text: str, command, primary: bool = False) -> tk.Button:
        background = self.BLUE if primary else self.PALE
        return tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 10, "bold"),
            bg=background, fg="#FFFFFF" if primary else self.BLUE_DARK,
            activebackground=self.BLUE_DARK if primary else "#DDE7FF",
            activeforeground="#FFFFFF" if primary else self.NAVY,
            padx=16, pady=9, relief="flat", bd=0, cursor="hand2",
            highlightthickness=2, highlightbackground=self.SURFACE,
            highlightcolor=self.ORANGE, takefocus=True,
        )

    def _entry(self, parent: tk.Widget, variable: tk.StringVar) -> tk.Entry:
        return tk.Entry(parent, textvariable=variable, font=("Segoe UI", 11),
                        fg=self.NAVY, bg=self.SURFACE, relief="solid", bd=1,
                        highlightthickness=2, highlightbackground=self.BORDER,
                        highlightcolor=self.BLUE)

    def _card(self, parent: tk.Widget, padding: int = 18) -> tk.Frame:
        return tk.Frame(parent, bg=self.SURFACE, padx=padding, pady=padding,
                        highlightbackground=self.BORDER, highlightthickness=1)

    def _build(self) -> None:
        top = tk.Frame(self, bg=self.NAVY, padx=32, pady=18)
        top.pack(fill="x")
        tk.Label(top, text="HISTORY STUDIO  /  PYTHON LAB", fg="#AFC6FB", bg=self.NAVY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(top, text="A browser history you can take apart", fg="#FFFFFF",
                 bg=self.NAVY, font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(4, 0))
        tk.Label(top, text="Back and Forward follow real previous and next links between Python nodes.",
                 fg="#DAE5FB", bg=self.NAVY, font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 0))

        workspace = tk.Frame(self, bg=self.BG, padx=20, pady=18)
        workspace.pack(fill="both", expand=True)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(0, weight=1)

        sidebar = self._card(workspace, 20)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        sidebar.configure(width=305)
        sidebar.grid_propagate(False)

        self._label(sidebar, "Controls", 16, True).pack(anchor="w")
        self._label(sidebar, "Open a page to extend the chain.", 10, color=self.MUTED).pack(anchor="w", pady=(3, 20))

        self._label(sidebar, "Page title", 10, True).pack(anchor="w")
        self.page_entry = self._entry(sidebar, self.title_input)
        self.page_entry.pack(fill="x", ipady=7, pady=(6, 10))
        self.page_entry.bind("<Return>", lambda _: self._visit())
        self._button(sidebar, "Visit page", self._visit, True).pack(fill="x")

        self._label(sidebar, "Navigate", 12, True).pack(anchor="w", pady=(24, 9))
        navigation = tk.Frame(sidebar, bg=self.SURFACE)
        navigation.pack(fill="x")
        navigation.grid_columnconfigure((0, 1), weight=1)
        self.back_button = self._button(navigation, "Back", lambda: self._action(
            self.history.back, "Moved back through previous."))
        self.back_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.forward_button = self._button(navigation, "Forward", lambda: self._action(
            self.history.forward, "Moved forward through next."))
        self.forward_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        tk.Frame(sidebar, height=1, bg=self.BORDER).pack(fill="x", pady=23)
        self._label(sidebar, "Structure tools", 12, True).pack(anchor="w")
        self._label(sidebar, "Positions start at 0.", 10, color=self.MUTED).pack(anchor="w", pady=(3, 12))
        self._label(sidebar, "Position", 10, True).pack(anchor="w")
        index_entry = self._entry(sidebar, self.index_input)
        index_entry.pack(fill="x", ipady=7, pady=(6, 10))
        self._button(sidebar, "Insert page at position", self._insert).pack(fill="x")
        self._button(sidebar, "Remove page at position", self._remove).pack(fill="x", pady=(8, 0))

        self._label(sidebar, "Tip", 10, True).pack(anchor="w", pady=(20, 4))
        tk.Label(sidebar, text="Go Back, then Visit page. The forward branch disappears.",
                 fg=self.MUTED, bg=self.SURFACE, font=("Segoe UI", 10),
                 justify="left", wraplength=250).pack(anchor="w")
        self._button(sidebar, "Restore example", lambda: self._action(
            self.history.reset, "Sample history restored.")).pack(fill="x", pady=(20, 0))
        self._button(sidebar, "Clear history", lambda: self._action(
            self.history.clear, "History cleared.")).pack(fill="x", pady=(8, 0))

        content = tk.Frame(workspace, bg=self.BG)
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        browser = self._card(content, 18)
        browser.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self._label(browser, "CURRENT PAGE", 9, True, color=self.BLUE).pack(anchor="w")
        self.current_title = self._label(browser, "", 21, True)
        self.current_title.pack(anchor="w", pady=(8, 4))
        self.current_hint = self._label(browser, "", 10, color=self.MUTED)
        self.current_hint.pack(anchor="w")

        structure = self._card(content, 18)
        structure.grid(row=1, column=0, sticky="nsew")
        structure.grid_columnconfigure(0, weight=1)
        structure.grid_rowconfigure(2, weight=1)
        heading = tk.Frame(structure, bg=self.SURFACE)
        heading.grid(row=0, column=0, sticky="ew")
        self._label(heading, "Node links", 16, True).pack(side="left")
        tk.Checkbutton(heading, text="View from tail", variable=self.reverse,
                       command=self._draw, font=("Segoe UI", 10), fg=self.BLUE,
                       bg=self.SURFACE, activebackground=self.SURFACE,
                       selectcolor=self.SURFACE, cursor="hand2", takefocus=True).pack(side="right")
        self._label(structure, "Blue arrow: next   •   Orange arrow: previous   •   Click a card to select",
                    10, color=self.MUTED).grid(row=1, column=0, sticky="w", pady=(5, 10))
        canvas_holder = tk.Frame(structure, bg=self.BG)
        canvas_holder.grid(row=2, column=0, sticky="nsew")
        canvas_holder.grid_columnconfigure(0, weight=1)
        canvas_holder.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(canvas_holder, bg=self.BG, highlightthickness=0, height=210)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<MouseWheel>", lambda event: self.canvas.xview_scroll(
            -1 if event.delta > 0 else 1, "units"))
        scroll = ttk.Scrollbar(canvas_holder, orient="horizontal", command=self.canvas.xview)
        scroll.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=scroll.set)

        bottom = tk.Frame(content, bg=self.BG)
        bottom.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)
        list_card = self._card(bottom, 14)
        list_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self._label(list_card, "History entries", 12, True).pack(anchor="w", pady=(0, 8))
        columns = ("position", "page", "previous", "next")
        self.table = ttk.Treeview(list_card, columns=columns, show="headings", height=6, selectmode="browse")
        for column, width in (("position", 62), ("page", 130), ("previous", 98), ("next", 98)):
            self.table.heading(column, text=column.title())
            self.table.column(column, width=width, anchor="w")
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self._choose_table_row)

        details = self._card(bottom, 14)
        details.grid(row=0, column=1, sticky="nsew")
        self._label(details, "Pointer inspector", 12, True).pack(anchor="w", pady=(0, 8))
        self.pointer_labels: dict[str, tk.Label] = {}
        for key, title in (("previous", "PREVIOUS"), ("current", "CURRENT"), ("next", "NEXT")):
            self._label(details, title, 9, True, color=self.BLUE).pack(anchor="w", pady=(5, 0))
            result = self._label(details, "", 11, True)
            result.pack(anchor="w")
            self.pointer_labels[key] = result

        footer = tk.Frame(self, bg=self.BG, padx=22, pady=10)
        footer.pack(fill="x")
        self.status = tk.Label(footer, textvariable=self.message, bg=self.BG, fg=self.MUTED,
                               font=("Segoe UI", 10), anchor="w")
        self.status.pack(fill="x")

    def _position(self) -> int:
        raw = self.index_input.get().strip()
        if not raw.isdecimal():
            raise ListError("Enter a non-negative whole number for the position.")
        return int(raw)

    def _action(self, operation, success: str) -> bool:
        try:
            operation()
        except ListError as error:
            self.message.set(str(error))
            self.status.configure(fg=self.ERROR)
            self.bell()
            return False
        self.message.set(success)
        self.status.configure(fg=self.BLUE_DARK)
        self._refresh()
        return True

    def _visit(self) -> None:
        title = self.title_input.get().strip()
        if self._action(lambda: self.history.visit(title),
                        f"Visited {title}. Any forward branch was cleared."):
            self.title_input.set("")

    def _insert(self) -> None:
        title = self.title_input.get().strip()
        if self._action(lambda: self.history.insert(self._position(), title),
                        f"Inserted {title}; neighboring links were updated."):
            self.title_input.set("")

    def _remove(self) -> None:
        self._action(lambda: self.history.remove(self._position()),
                     "Page removed; neighboring links were reconnected.")

    def _choose_table_row(self, _: tk.Event) -> None:
        if self._updating_table:
            return
        chosen = self.table.selection()
        if chosen and self.history.pages.cursor is not self.history.pages._node_at(int(chosen[0])):
            self._action(lambda: self.history.select(int(chosen[0])),
                         f"Selected page at position {chosen[0]}.")

    def _refresh(self) -> None:
        state = self.history.snapshot()
        nodes = state["nodes"]
        selected = next((node for node in nodes if node["selected"]), None)
        self.current_title.configure(text=state["cursor"] or "No page open")
        self.current_hint.configure(text=f"{state['size']} page(s) in history  •  "
                                    "Open a page after going Back to replace the forward branch.")
        self.pointer_labels["previous"].configure(text=selected["previous"] or "NULL" if selected else "NULL")
        self.pointer_labels["current"].configure(text=selected["value"] if selected else "NULL")
        self.pointer_labels["next"].configure(text=selected["next"] or "NULL" if selected else "NULL")
        self.back_button.configure(state="normal" if selected and selected["previous"] is not None else "disabled")
        self.forward_button.configure(state="normal" if selected and selected["next"] is not None else "disabled")
        self._updating_table = True
        for item in self.table.get_children():
            self.table.delete(item)
        for node in nodes:
            self.table.insert("", "end", iid=str(node["index"]),
                              values=(node["index"], node["value"],
                                      node["previous"] or "NULL", node["next"] or "NULL"))
        if selected:
            self.table.selection_set(str(selected["index"]))
            self.table.see(str(selected["index"]))
        self._updating_table = False
        self._draw()

    def _draw(self) -> None:
        canvas = self.canvas
        canvas.delete("all")
        nodes = self.history.snapshot()["nodes"]
        if not nodes:
            canvas.create_text(40, 110, text="No pages yet. Visit a page to build the history.",
                               anchor="w", fill=self.MUTED, font=("Segoe UI", 13))
            canvas.configure(scrollregion=(0, 0, max(canvas.winfo_width(), 700), 220))
            return
        visible = list(reversed(nodes)) if self.reverse.get() else nodes
        card_width, step, left, top = 160, 220, 35, 53
        canvas.create_text(left, 20, anchor="w", fill=self.BLUE, font=("Segoe UI", 9, "bold"),
                           text="TAIL TO HEAD" if self.reverse.get() else "HEAD TO TAIL")
        for order, node in enumerate(visible):
            x = left + order * step
            active = node["selected"]
            card = canvas.create_rectangle(x, top, x + card_width, top + 104,
                                           fill=self.PALE if active else self.SURFACE,
                                           outline=self.BLUE if active else self.BORDER,
                                           width=3 if active else 2)
            number = canvas.create_text(x + 13, top + 22, text=f"PAGE {node['index']:02d}",
                                        anchor="w", fill=self.MUTED, font=("Segoe UI", 9, "bold"))
            title = canvas.create_text(x + 13, top + 61, text=node["value"], width=card_width - 24,
                                       anchor="w", fill=self.NAVY, font=("Segoe UI", 13, "bold"))
            tag = canvas.create_text(x + 13, top + 88, anchor="w",
                                     text="● CURRENT" if active else "HISTORY NODE",
                                     fill=self.BLUE if active else self.MUTED,
                                     font=("Segoe UI", 8, "bold"))
            for item in (card, number, title, tag):
                canvas.tag_bind(item, "<Button-1>", lambda _, index=node["index"]:
                                self._action(lambda: self.history.select(index),
                                             f"Selected page at position {index}."))
            if order + 1 < len(visible):
                start = x + card_width + 8
                canvas.create_line(start, top + 40, start + 42, top + 40, fill=self.BLUE,
                                   width=3, arrow=tk.LAST)
                canvas.create_line(start + 42, top + 68, start, top + 68, fill=self.ORANGE,
                                   width=3, arrow=tk.LAST)
        canvas.configure(scrollregion=(0, 0, max(canvas.winfo_width(), left + len(visible) * step), 220))


if __name__ == "__main__":
    HistoryApp().mainloop()
