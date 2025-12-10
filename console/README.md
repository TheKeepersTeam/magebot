# MageBot

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

MageBot is a magical duel game inspired by the Harry Potter universe, where you face an artificial intelligence using spells. Developed by the ZIOS team.

## Features

- **Magical Duel Against AI** : Spell system (attack, healing, resistance) with resource management (HP, Resistance, Mana).
- **Available Versions** :
  - Console : Complete and advanced version for command-line duels.
  - Discord : (Upcoming) Integration with Discord API for community interactions.
  - Browser : (Under study) Web version with 2D graphics.
- **Intelligent AI** : Uses a Minimax algorithm for strategic decisions, considering HP, resistance, and mana.
- **Progression and Statistics** : (Upcoming) Rankings, game saves.

## Installation

1. Clone the repository :
   ```bash
   git clone https://github.com/your-username/magebot.git
   cd magebot
   ```

2. Install dependencies :
   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies** : `colorama` for console text coloring.

## Usage

- **Console Version** (recommended, most advanced) :
  ```bash
  python MageBot/console_version/magebotcli.py
  ```
  Type `help` for available commands, `start_dual` to start a duel against the AI.

- **Discord Version** : (Upcoming) Add the bot to your server and use commands.
- **Web Version** : (Upcoming) Open in a browser.

## Changelog

| Date       | Version | New Features / Modifications |
|------------|---------|------------------------------|
| 2025-12-10 | 1.1.4   | AI improvements (mana/resistance in heuristic, avoid healing at max HP), colored startup UI, added 'about' command, console version is the most advanced |
| 2025-09-24 | 0.1.0   | Project creation, initial console and Discord features |

## Contributors

- ZIOS Team : Development and maintenance.

## License

This project is under the MIT license. See the LICENSE file for more details.
