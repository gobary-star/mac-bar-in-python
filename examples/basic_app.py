"""Minimal example of BAD KITTY MacBar."""

import tkinter as tk
from macbar import MacBar

root = tk.Tk()
root.geometry("900x600+120+100")
root.minsize(480, 320)

app = MacBar(root, title="BAD KITTY MacBar", status="Ready", background="#202124")
app.pack(fill="both", expand=True)

heading = tk.Label(
    app.content,
    text="Your app starts here",
    font=("Segoe UI", 22, "bold"),
    bg="#202124",
    fg="#f2f2f2",
)
heading.pack(pady=(90, 12))

message = tk.Label(
    app.content,
    text="Add your own Tkinter widgets inside app.content.",
    font=("Segoe UI", 11),
    bg="#202124",
    fg="#b7bac2",
)
message.pack()

root.mainloop()
