"""A lightweight, macOS-inspired title bar for Tkinter applications.

This is an independent project and is not affiliated with Apple.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional


class MacBar(tk.Frame):
    """A draggable, borderless Tkinter window with traffic-light controls.

    Use this frame as the root window's main child. Add application widgets to
    ``app.content``. The root window is switched to ``overrideredirect`` mode.

    Args:
        master: A ``tk.Tk`` or ``tk.Toplevel`` window.
        title: Text displayed in the title bar.
        background: Background color for the bar and content frame.
        title_color: Title text color.
        status: Optional small status label shown beside the title.
        height: Title-bar height in pixels.
    """

    COLORS = {"close": "#ff5f57", "minimize": "#febc2e", "maximize": "#28c840"}
    HOVER_COLORS = {"close": "#ff817a", "minimize": "#ffd166", "maximize": "#58dc6a"}

    def __init__(
        self,
        master: tk.Misc,
        title: str = "BAD KITTY App",
        background: str = "#202124",
        title_color: str = "#f2f2f2",
        status: Optional[str] = None,
        height: int = 42,
        **kwargs,
    ) -> None:
        super().__init__(master, bg=background, bd=0, highlightthickness=0, **kwargs)
        self.window = master.winfo_toplevel()
        self.background = background
        self.title_color = title_color
        self.title = title
        self.status = status
        self.bar_height = max(32, int(height))
        self._drag_x = 0
        self._drag_y = 0
        self._restore_geometry: Optional[str] = None
        self._maximized = False
        self._was_iconified = False
        self._map_after_id: Optional[str] = None

        self.window.overrideredirect(True)
        self.window.configure(bg=background)

        self.bar = tk.Frame(self, bg=background, height=self.bar_height, bd=0)
        self.bar.pack(fill="x")
        self.bar.pack_propagate(False)

        self.controls = tk.Canvas(
            self.bar, width=76, height=self.bar_height, bg=background,
            bd=0, highlightthickness=0, relief="flat"
        )
        self.controls.pack(side="left", padx=(10, 0))
        self._draw_controls()

        self.title_label = tk.Label(
            self.bar, text=title, bg=background, fg=title_color,
            font=("Segoe UI", 10, "bold"), anchor="center"
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status_label = None
        if status:
            self.status_label = tk.Label(
                self.bar, text=status, bg=background, fg="#a8abb2",
                font=("Segoe UI", 8), anchor="w"
            )
            self.status_label.pack(side="right", padx=(0, 12))

        self.content = tk.Frame(self, bg=background, bd=0, highlightthickness=0)
        self.content.pack(fill="both", expand=True)

        for widget in (self.bar, self.title_label):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag_window)
        if self.status_label:
            self.status_label.bind("<ButtonPress-1>", self._start_drag)
            self.status_label.bind("<B1-Motion>", self._drag_window)

        self.window.bind("<Map>", self._on_map, add="+")
        self.window.bind("<Escape>", lambda _event: self.close(), add="+")

    def _draw_controls(self) -> None:
        """Draw the three controls as canvas ovals (no image resources needed)."""
        self._control_items = {}
        y = self.bar_height / 2
        for index, name in enumerate(("close", "minimize", "maximize")):
            x = 10 + index * 22
            item = self.controls.create_oval(
                x, y - 6, x + 12, y + 6,
                fill=self.COLORS[name], outline=self.COLORS[name], width=1,
                tags=(name,)
            )
            self._control_items[name] = item
            self.controls.tag_bind(name, "<Button-1>", lambda event, action=name: self._control_click(action))
            self.controls.tag_bind(name, "<Enter>", lambda event, action=name: self._set_hover(action, True))
            self.controls.tag_bind(name, "<Leave>", lambda event, action=name: self._set_hover(action, False))

    def _set_hover(self, name: str, hovered: bool) -> None:
        color = self.HOVER_COLORS[name] if hovered else self.COLORS[name]
        item = self._control_items.get(name)
        if item is not None:
            self.controls.itemconfigure(item, fill=color, outline=color)

    def _control_click(self, action: str) -> None:
        if action == "close":
            self.close()
        elif action == "minimize":
            self.minimize()
        elif action == "maximize":
            self.toggle_maximize()

    def _start_drag(self, event: tk.Event) -> None:
        if self._maximized:
            return
        self._drag_x = event.x_root - self.window.winfo_x()
        self._drag_y = event.y_root - self.window.winfo_y()

    def _drag_window(self, event: tk.Event) -> None:
        if self._maximized or self._was_iconified:
            return
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.window.geometry(f"+{x}+{y}")

    def minimize(self) -> None:
        """Minimize the window while temporarily restoring native decorations."""
        try:
            self._was_iconified = True
            self.window.overrideredirect(False)
            self.window.iconify()
        except tk.TclError:
            self._was_iconified = False
            self.window.overrideredirect(True)

    def toggle_maximize(self) -> None:
        """Toggle between the current geometry and the available screen area."""
        try:
            if not self._maximized:
                self._restore_geometry = self.window.geometry()
                self.window.update_idletasks()
                width = self.window.winfo_screenwidth()
                height = self.window.winfo_screenheight()
                self.window.geometry(f"{width}x{height}+0+0")
                self._maximized = True
            else:
                if self._restore_geometry:
                    self.window.geometry(self._restore_geometry)
                self._maximized = False
        except tk.TclError:
            pass

    def close(self) -> None:
        """Close the associated top-level window."""
        try:
            self.window.destroy()
        except tk.TclError:
            pass

    def set_title(self, title: str) -> None:
        """Update the title text."""
        self.title = title
        self.title_label.configure(text=title)

    def set_status(self, status: Optional[str]) -> None:
        """Set or clear the optional status text."""
        self.status = status
        if status:
            if self.status_label is None or not self.status_label.winfo_exists():
                self.status_label = tk.Label(
                    self.bar, text=status, bg=self.background, fg="#a8abb2",
                    font=("Segoe UI", 8), anchor="w"
                )
                self.status_label.pack(side="right", padx=(0, 12))
                self.status_label.bind("<ButtonPress-1>", self._start_drag)
                self.status_label.bind("<B1-Motion>", self._drag_window)
            else:
                self.status_label.configure(text=status)
        elif self.status_label is not None:
            self.status_label.destroy()
            self.status_label = None

    def _on_map(self, _event: tk.Event) -> None:
        """Re-enable the custom title bar after the window is restored."""
        if not self._was_iconified:
            return
        if self._map_after_id:
            try:
                self.window.after_cancel(self._map_after_id)
            except tk.TclError:
                pass
        self._map_after_id = self.window.after_idle(self._finish_restore)

    def _finish_restore(self) -> None:
        self._map_after_id = None
        try:
            if self.window.state() == "iconic":
                return
            self.window.overrideredirect(True)
            self._was_iconified = False
        except tk.TclError:
            self._was_iconified = False


__all__ = ["MacBar"]
