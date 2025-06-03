
# 🚀 Flixer - Typing Game Bot

Flixer is a powerful Python bot designed to automate typing across popular online typing games using Selenium and other tools. It includes a rich TUI (text-based user interface) powered by `rich`.

## 🎮 Supported Games

- Nitro Type
- Type Racer
- Key Mash
- MonkeyType
- Human Benchmark (Typing Test)
- Typer.io

---

## 🛠️ Features

- Typing automation with adjustable speed
- Game menu with command interface
- Auto-installs required packages
- Uses keyboard shortcuts to start typing
- Logs all activity with timestamps
- Configuration file support for speed settings
- Restart, clear, and navigation commands

---

## 📦 Requirements

The script auto-installs these packages:

```
rich
selenium
bs4
keyboard
pyautogui
webdriver-manager
```

You'll also need:

- Google Chrome browser
- Python 3.7+

---

## ▶️ Usage

1. **Run the Script**

```bash
python flixer.py
```

2. **Main Menu Commands**

- `1`, `2`, `3` → Launch game (based on page)
- `next`, `prev` → Switch between pages of games
- `help`, `clist`, `commands` → Show help or command list
- `speed` → Set typing speed in seconds per character
- `restart` → Restart via batch script (`start.bat`)
- `exit`, `clear`, `version`

3. **Start Typing**

When the game loads, press `CTRL + ALT + P` to begin the automated typing.

---

## ⚙️ Configuration

Config is saved in `config/config.json`:

```json
{
  "typing_speed": 0.05
}
```

You can modify this manually or via the `speed` command in the program.

---

## 📁 Logs

All logs are saved in the `logs/` folder with timestamps:

- `.log` → Typing actions
- `.info` → Informational logs

---

## 📄 License

MIT License. Use responsibly. Automating typing games may violate their terms of service.
