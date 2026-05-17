"""Render a policy dict + sections list to HTML using the Jinja2 template."""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(metadata: dict, sections: list[dict], templates_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"]),
    )
    # tojson filter is built-in to Jinja2's Environment
    template = env.get_template("policy.html.j2")
    return template.render(policy=metadata, sections=sections)
