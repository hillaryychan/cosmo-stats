import os

# Typer forces ANSI colours when GITHUB_ACTIONS, FORCE_COLOR, or PY_COLORS is set.
# Disable it so CLI output assertions can compare plain text.
os.environ["_TYPER_FORCE_DISABLE_TERMINAL"] = "1"
