# BAD KITTY MacBar

A lightweight, reusable macOS-inspired title bar for Python Tkinter applications. It provides a draggable header, traffic-light controls, a centered title, and minimize/maximize/close actions without external Python packages.

> Independent community project inspired by the visual style of macOS. It is not affiliated with or endorsed by Apple.

## Requirements

- Python 3.10 or newer
- Tkinter (included with most standard Python installations)

## Quick start

```python
import tkinter as tk
from macbar import MacBar

root = tk.Tk()
root.geometry("900x600")

app = MacBar(root, title="My application", background="#202124")
app.pack(fill="both", expand=True)

content = tk.Frame(app.content, bg="#202124")
content.pack(fill="both", expand=True, padx=24, pady=24)
tk.Label(content, text="Hello from Tkinter", bg="#202124", fg="white").pack()

root.mainloop()
```

## Features

- macOS-inspired red, yellow, and green window controls
- Drag the window from the title bar
- Minimize, maximize/restore, and close controls
- Centered title and optional status text
- No third-party dependencies
- Reusable `MacBar` frame with an `app.content` area for your widgets

## Notes

Window-manager behavior differs between Windows, macOS, and Linux. Test minimize and maximize behavior on your target operating system. Rounded corners are controlled by the operating system and are not guaranteed by Tkinter itself.

## Contributing

Bug reports, fixes, examples, and improvements are welcome. Keep changes focused and test them on your platform when possible. Please include **JD** or **JV** in the credits when redistributing or extending this project, as requested by the original project author.

## License

MIT. See [LICENSE](LICENSE).

## Credits

Created by **JD / JV**. BAD KITTY project.
