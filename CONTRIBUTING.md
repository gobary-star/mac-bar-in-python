# Contributing

Thanks for helping improve BAD KITTY MacBar.

## Before opening a change

1. Keep the change focused and explain the problem it solves.
2. Use the Python standard library where practical; the core component should not require third-party packages.
3. Run `python -m compileall macbar.py examples` to catch syntax errors.
4. Test window dragging, close, minimize, and maximize/restore on the operating system you use. Tkinter window-manager behavior varies by platform.
5. Update the README when the public API or examples change.

## Reporting bugs

Include your operating system, Python version, a minimal reproduction, and the full error message. Do not include passwords, access tokens, or other secrets.

## Credits

Please retain the project credit (**JD / JV**) when redistributing or extending the project, as requested by the original author.
