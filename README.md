**FLICKER: Capture Memories in a Flash ✨**

**FLICKER** is a versatile screenshot application for Linux that empowers you to seamlessly capture, organize, and cherish those fleeting moments on your screen.

**FLICKER** stands for **Fast Linux Interface for Capturing & Keeping Exceptionally Radiant screenshots**. Corny.

**Features:**

- Capture full screen, specific windows, or custom selections with ease.
 - Save screenshots in a dedicated `Pictures/FLICKERs` folder by default.
 - Set the `FLICKER_DIR` environment variable to use a custom save location.
- Support for both X11 and Wayland display servers.
- Intuitive keyboard shortcuts for lightning-fast capture:
    - WIN + Shift + S (or ALT + Shift + S / F6): Capture a selection
    - WIN + Shift + W (or ALT + Shift + W / F9): Capture the focused window
    - F7: Capture the screen under the cursor
    - WIN + Shift + D (or ALT + Shift + D / F8): Capture all screens
 - Screenshots are automatically copied to the clipboard and a desktop
   notification confirms the save location
- A program icon is provided in `resources/flicker.png` and installed with the package.

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
3. To install the packaged release on Debian/Ubuntu based systems run:
   ```bash
   sudo dpkg -i flicker_<version>_all.deb
   sudo apt-get -f install  # installs any missing dependencies
   ```
   The package declares dependencies on `PyQt5` and `pynput`, so `apt-get -f install` will automatically fetch them if they are not present.

### Building the Debian package

To build a Debian package from this source tree install the required build
dependencies and run the Debian tools from the packaging directory:

```bash
cd packaging
sudo apt-get build-dep .
# or install the helper
sudo apt-get install python3-build
dpkg-buildpackage -us -uc -b
```

The resulting `.deb` will appear one directory above `packaging`.

**Usage:**

1. Launch the application:
   ```bash
   python -m flicker.app
   ```
2. Use the keyboard shortcuts to capture screenshots:
    - WIN + Shift + S (or ALT + Shift + S / F6): Capture a selection
    - WIN + Shift + W (or ALT + Shift + W / F9): Capture the focused window
    - F7: Capture the screen under the cursor
    - WIN + Shift + D (or ALT + Shift + D / F8): Capture all screens

You can also call ``grab-screen`` directly for one-off captures. By default it
lets you select a region and then opens the result with your desktop image
viewer. Use ``--full``, ``--screen`` or ``--window`` to change the mode. Run
``grab-screen --list-monitors`` to see available monitors or ``--monitor 2`` to
capture a specific display.

### Running as a background service

Copy ``flicker.service`` to ``~/.config/systemd/user/`` and enable it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now flicker.service
```

This starts the hotkey listener automatically on login.

**Planned Features:**

- Customizable save locations and filename conventions.
- Annotations and editing tools for screenshots.
- Graphical user interface (GUI) for enhanced user experience.
- Better support for X11 and Wayland

**Contributing:**

Your contributions are warmly welcomed! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

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
