# Gathering-bot

A Python bot that automates wood-cutting in an RSPS (RuneScape private server) sandbox, using screen-reading (no game memory access or network injection). Built as a learning project to explore computer vision (HSV color masking, contour detection) and OCR-based game-state verification.

⚠️ **Educational use only.** This was built and tested against a locally-hosted private server (RSPSApp/tsps) under my own control. **Do not run this against a live, official game server** — using automation/bots on real game accounts violates nearly every game's Terms of Service and will likely get your account banned. This project exists to learn computer vision and automation concepts, not to cheat in any live game.

## How it works

- **Detection** (`detection.py`): finds trees on screen using HSV color masking (green canopy + brown trunk check) combined with contour shape/density filtering.
- **Chat verification** (`chat.py`): reads the in-game chat log via OCR (Tesseract) to confirm whether a chop succeeded, failed, or the inventory is full — instead of blindly guessing with timers.
- **Orchestration** (`bot.py`): the main loop — find a tree, click it, wait for confirmation via chat, repeat. Wanders to a new area if no tree is currently visible.

## Setup

1. Install Python dependencies:

pip install -r requirements.txt

2. Install Tesseract OCR (required by `pytesseract`, not pip-installable): https://github.com/UB-Mannheim/tesseract/wiki
3. Update `TESSERACT_PATH` and `CHAT_REGION` in `config.py` to match your own Tesseract install location and screen resolution.
4. Run:

python bot.py

   Press **F12** at any time to stop the bot (panic key).

## Tools

The `tools/` folder contains development/debugging scripts used to tune detection (color sampling, mask visualization, contour debugging) — not needed to run the bot itself.
