# Telegram Bot

This project contains a Telegram bot and related helper scripts.

## `private_data/` directory

Configuration files containing private data such as bot tokens are stored in the `private_data/` folder. This directory is excluded from version control via `.gitignore` so that credentials do not get committed.

Place your `.env` file inside `private_data/`. It may define the following variables:

```
BOT_TOKEN=<token used on Linux/macOS>
BOT_TOKEN_WIN=<token used on Windows>
```
At least one of these tokens must be present for the bot to start. The
`config.py` file loads this `.env` file automatically. Whichever token is set
will be used; if both are provided the one appropriate for the current
platform is chosen.
