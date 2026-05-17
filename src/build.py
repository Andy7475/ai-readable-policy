"""Build pipeline: Markdown policies -> HTML + search-index.json in dist/."""
import shutil
from pathlib import Path

from policy_parser import parse
from html_renderer import render
from index_builder import build as build_index

REPO_ROOT = Path(__file__).parent.parent
POLICIES_DIR = REPO_ROOT / "policies"
TEMPLATES_DIR = REPO_ROOT / "templates"
WEB_DIR = REPO_ROOT / "web"
DIST_DIR = REPO_ROOT / "dist"


def main() -> None:
    # Prepare dist/
    dist_policies = DIST_DIR / "policies"
    dist_policies.mkdir(parents=True, exist_ok=True)

    all_policies = []

    for md_path in sorted(POLICIES_DIR.glob("*.md")):
        print(f"Processing {md_path.name}...")
        metadata, sections = parse(md_path)

        html = render(metadata, sections, TEMPLATES_DIR)
        out_name = md_path.stem + ".html"
        out_path = dist_policies / out_name
        out_path.write_text(html, encoding="utf-8")
        print(f"  Wrote {out_path.relative_to(REPO_ROOT)}")

        all_policies.append({"metadata": metadata, "sections": sections})

    build_index(all_policies, DIST_DIR / "search-index.json")

    # Copy web assets
    for asset in WEB_DIR.iterdir():
        dest = DIST_DIR / asset.name
        shutil.copy2(asset, dest)
        print(f"  Copied {asset.name} -> dist/")

    print(f"\nBuild complete: {DIST_DIR}")


if __name__ == "__main__":
    main()
