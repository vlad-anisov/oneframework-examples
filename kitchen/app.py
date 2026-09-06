"""Kitchen sink: every component the framework offers, in one installable app."""

from pathlib import Path

from oneframework import App, load_all

modules = load_all(Path(__file__).parent / "modules")

app = App(modules=modules, title="Kitchen", color="#6750A4")
