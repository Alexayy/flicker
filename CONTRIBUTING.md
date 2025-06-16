# Contributing to Flicker

Thank you for your interest in improving **Flicker**! This document describes how to get the project running locally, the coding style used, and how to submit patches or issues.

## Setting up the Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/Alexayy/flicker
   cd flicker
   ```
2. **Create a virtual environment (optional but recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r flicker/requirements.txt
   ```
4. **Install developer tools** (optional)
   ```bash
   pip install flake8
   ```
5. **Run the linter** to check code style:
   ```bash
   make lint
   ```
6. **Run Flicker** to verify everything works:
   ```bash
   python -m flicker.app
   ```

## Coding Style

* Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.
* Use 4 spaces per indentation level and include type hints where appropriate.
* Keep functions short and well documented with docstrings.
* Run `flake8` or similar tools before submitting if available.

## Submitting Patches

1. Fork the repository on GitHub and create a feature branch for your change.
2. Make your changes with clear commit messages.
3. Ensure your code runs locally and all tests pass if applicable.
4. Open a pull request against `main` with a description of the changes.

## Reporting Issues

Bug reports and feature requests are tracked using GitHub Issues. When filing a new issue, please include:

* A clear description of the problem or request.
* Steps to reproduce if reporting a bug.
* The version of Flicker and your operating system if relevant.

We appreciate all contributions, big or small. Thank you for helping make Flicker better!
