"""Build pipeline: Markdown policies -> HTML + search-index.json in dist/."""
import json
import shutil
from pathlib import Path

from policy_parser import parse
from html_renderer import render
from index_builder import build as build_index
from process_renderer import parse as parse_process, render as render_process

REPO_ROOT = Path(__file__).parent.parent
POLICIES_DIR = REPO_ROOT / "policies"
PROCESSES_DIR = REPO_ROOT / "processes"
TEMPLATES_DIR = REPO_ROOT / "templates"
WEB_DIR = REPO_ROOT / "web"
DIST_DIR = REPO_ROOT / "dist"


def main() -> None:
    dist_policies = DIST_DIR / "policies"
    dist_policies.mkdir(parents=True, exist_ok=True)
    dist_processes = DIST_DIR / "processes"
    dist_processes.mkdir(parents=True, exist_ok=True)

    # ── Policies ─────────────────────────────────────────────────────────────
    all_policies = []
    for md_path in sorted(POLICIES_DIR.glob("*.md")):
        print(f"Processing {md_path.name}...")
        metadata, sections = parse(md_path)
        html = render(metadata, sections, TEMPLATES_DIR)
        out_path = dist_policies / (md_path.stem + ".html")
        out_path.write_text(html, encoding="utf-8")
        print(f"  Wrote {out_path.relative_to(REPO_ROOT)}")
        all_policies.append({"metadata": metadata, "sections": sections, "file_stem": md_path.stem})

    index_path = DIST_DIR / "search-index.json"
    build_index(all_policies, index_path)

    # ── Processes ─────────────────────────────────────────────────────────────
    search_index = json.loads(index_path.read_text(encoding="utf-8"))
    for yaml_path in sorted(PROCESSES_DIR.glob("*.yaml")):
        print(f"Processing {yaml_path.name}...")
        process = parse_process(yaml_path)
        html = render_process(process, TEMPLATES_DIR, search_index)
        out_path = dist_processes / (yaml_path.stem + ".html")
        out_path.write_text(html, encoding="utf-8")
        print(f"  Wrote {out_path.relative_to(REPO_ROOT)}")

    # ── Web assets ────────────────────────────────────────────────────────────
    for asset in WEB_DIR.iterdir():
        dest = DIST_DIR / asset.name
        shutil.copy2(asset, dest)
        print(f"  Copied {asset.name} -> dist/")

    print(f"\nBuild complete: {DIST_DIR}")


if __name__ == "__main__":
    main()
