"""Entry point: load every module folder, then start."""

from pathlib import Path

from oneframework import App, load_all

modules = load_all(Path(__file__).parent / "modules")

app = App(modules=modules, title="Modular", color="#00696E")
