**Here's a README.md draft for your Linux screenshot app, incorporating best practices and addressing potential issues:**

**# FLICKER: Capture Memories in a Flash ✨**

**FLICKER** is a versatile screenshot application for Linux that empowers you to seamlessly capture, organize, and cherish those fleeting moments on your screen.

**FLICKER** stands for **Fast Linux Interface for Capturing & Keeping Exceptionally Radiant screenshots**. Corny.

**Features:**

- Capture full screen, specific windows, or custom selections with ease.
- Save screenshots in a dedicated `Pictures/FLICKERs` folder for effortless organization.
- Support for both X11 and Wayland display servers.
- Intuitive keyboard shortcuts for lightning-fast capture:
    - ALT + Shift + S (F9): Capture a selection
    - ALT + Shift + W (F10): Capture the current window
    - ALT + Shift + D (F11): Capture the entire screen

**Installation:**

1. Clone this repository:
   ```bash
   git clone https://github.com/Alexayy/flicker
   ```
2. Install required dependencies:
   ```bash
   cd flicker
   pip install -r requirements.txt
   ```

**Usage:**

1. Launch the application:
   ```bash
   python app.py
   ```
2. Use the keyboard shortcuts to capture screenshots:
    - ALT + Shift + S (F9): Capture a selection
    - ALT + Shift + W (F10): Capture the current window
    - ALT + Shift + D (F11): Capture the entire screen

**Planned Features:**

- Customizable save locations and filename conventions.
- Annotations and editing tools for screenshots.
- Graphical user interface (GUI) for enhanced user experience.
- Copy to clipboard
- Better support for X11 and Wayland

**Contributing:**

Your contributions are warmly welcomed! Please refer to the CONTRIBUTING.md for guidelines - when CONTRIBUTING.md gets written, that is...

**Built With:**

- Python
- PyQt5
- pynput
- grim (for Wayland)
- import (for X11)

**License:**

MIT License

**Contact:**

For questions, feedback, or collaboration, please reach out to [aleksa.cakic@gmail.com].
