"""Parse process YAML files and render to HTML with embedded Mermaid diagram."""
import json
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


def parse(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _wrap_label(text: str, width: int = 38) -> str:
    """Wrap text at word boundaries using mermaid <br/> line breaks."""
    words = text.split()
    lines, current, current_len = [], [], 0
    for word in words:
        extra = 1 if current else 0
        if current and current_len + extra + len(word) > width:
            lines.append(" ".join(current))
            current, current_len = [word], len(word)
        else:
            current.append(word)
            current_len += extra + len(word)
    if current:
        lines.append(" ".join(current))
    return "<br/>".join(lines)


def to_mermaid(process: dict) -> str:
    """Generate a Mermaid flowchart string from a process definition."""
    lines = ["flowchart TD"]
    nodes = process.get("nodes", {})

    for node_id, node in nodes.items():
        node_type = node.get("type", "question")
        # Questions get the full text; action/terminal nodes get a shorter excerpt
        raw = node.get("question") or node.get("text", node_id)
        raw = " ".join(raw.strip().split())  # collapse whitespace
        if node_type != "question" and len(raw) > 120:
            raw = raw[:117] + "..."
        label = _wrap_label(raw).replace('"', "'")

        node_type = node.get("type", "question")
        outcome = node.get("outcome", "")

        if node_type == "terminal" and outcome == "approved":
            shape = f'(["{label}"])'
        elif node_type == "terminal" and outcome == "blocked":
            shape = f'[/"{label}"\\]'
        elif node_type == "action":
            shape = f'{{"{label}"}}'
        else:
            shape = f'["{label}"]'

        lines.append(f"  {node_id}{shape}")

        for opt in node.get("options", {}).values():
            edge_label = opt["label"].replace('"', "'")
            lines.append(f'  {node_id} -->|"{edge_label}"| {opt["next"]}')

        if "next" in node:
            lines.append(f"  {node_id} --> {node['next']}")

    # Style terminal nodes
    approved_ids = [nid for nid, n in nodes.items() if n.get("outcome") == "approved"]
    blocked_ids = [nid for nid, n in nodes.items() if n.get("outcome") == "blocked"]
    if approved_ids:
        lines.append(f"  style {' style '.join(approved_ids + [''])}".rstrip())
        for nid in approved_ids:
            lines.append(f"  style {nid} fill:#d4edda,stroke:#28a745,color:#155724")
    for nid in blocked_ids:
        lines.append(f"  style {nid} fill:#f8d7da,stroke:#dc3545,color:#721c24")

    return "\n".join(lines)


def render(process: dict, templates_dir: Path, search_index: dict | None = None) -> str:
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"]),
    )
    mermaid = to_mermaid(process)

    chunk_map = {}
    if search_index:
        chunk_map = {c["section_id"]: c for c in search_index.get("chunks", [])}

    return env.get_template("process.html.j2").render(
        process=process,
        mermaid=mermaid,
        nodes_json=json.dumps(process.get("nodes", {})),
        chunk_map_json=json.dumps(chunk_map),
    )
