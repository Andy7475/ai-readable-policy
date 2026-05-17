"""Parse a policy Markdown file into metadata and section dicts."""
import re
from pathlib import Path

import markdown
import yaml
from bs4 import BeautifulSoup
from slugify import slugify


def parse(path: Path) -> tuple[dict, list[dict]]:
    """Return (metadata, sections) for the given Markdown policy file."""
    raw = path.read_text(encoding="utf-8")
    metadata, body = _split_frontmatter(raw)
    sections = _extract_sections(metadata["id"], body)
    return metadata, sections


def _split_frontmatter(raw: str) -> tuple[dict, str]:
    """Split YAML front matter from Markdown body."""
    if not raw.startswith("---"):
        raise ValueError("Policy file must start with YAML front matter (---)")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Could not find closing --- for front matter")
    metadata = yaml.safe_load(parts[1])
    body = parts[2].strip()
    return metadata, body


def _extract_sections(policy_id: str, body: str) -> list[dict]:
    """Convert Markdown body to a list of section dicts, one per ## heading."""
    html = markdown.markdown(body, extensions=["extra"])
    soup = BeautifulSoup(html, "html.parser")

    sections = []
    current_heading = None
    current_nodes = []

    for node in soup.children:
        if node.name == "h2":
            if current_heading is not None:
                sections.append(_build_section(policy_id, current_heading, current_nodes))
            current_heading = node.get_text()
            current_nodes = []
        elif current_heading is not None:
            current_nodes.append(node)

    if current_heading is not None:
        sections.append(_build_section(policy_id, current_heading, current_nodes))

    return sections


def _build_section(policy_id: str, heading: str, nodes: list) -> dict:
    section_slug = slugify(heading, separator="-")
    section_id = f"{policy_id}--{section_slug}"
    content_html = "".join(str(n) for n in nodes)
    plain_text = " ".join(
        BeautifulSoup(content_html, "html.parser").get_text(" ").split()
    )
    return {
        "id": section_id,
        "title": heading,
        "content_html": content_html,
        "plain_text": plain_text,
    }
