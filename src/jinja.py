import pathlib
from typing import Optional

from jinja2 import Environment, FileSystemLoader, Template

from src.paths import TEMPLATE_DIR


def read_template(
    name: str, template_dir: pathlib.Path = TEMPLATE_DIR, globals: Optional[dict] = None
) -> Template:
    env = Environment(
        loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
    )
    if globals:
        env.globals.update(globals)
    return env.get_template(name)
