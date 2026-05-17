"""Build search-index.json from all parsed policy data."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "shall", "can",
    "not", "this", "that", "these", "those", "it", "its", "their", "they",
    "all", "any", "each", "both", "few", "more", "most", "other", "into",
    "through", "than", "so", "if", "no", "up", "out", "about", "such",
}


def _tokenise(text: str) -> list[str]:
    words = re.findall(r"[a-z]{3,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def build(all_policies: list[dict], output_path: Path) -> None:
    """
    all_policies: list of {metadata: dict, sections: list[dict]}
    Writes search-index.json to output_path.
    """
    policies_meta = []
    chunks = []

    for entry in all_policies:
        meta = entry["metadata"]
        policy_file = f"policies/{meta['id'].replace('_', '-')}.html"

        policies_meta.append({
            "id": meta["id"],
            "title": meta["title"],
            "file": policy_file,
            "version": str(meta.get("version", "")),
            "date": str(meta.get("date", "")),
            "owner": str(meta.get("owner", "")),
        })

        for section in entry["sections"]:
            chunks.append({
                "section_id": section["id"],
                "policy_id": meta["id"],
                "policy_file": policy_file,
                "policy_title": meta["title"],
                "section_title": section["title"],
                "text": section["plain_text"],
                "terms": _tokenise(section["plain_text"]),
            })

    index = {
        "version": 1,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "policies": policies_meta,
        "chunks": chunks,
    }

    output_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"  Wrote {len(chunks)} chunks to {output_path}")
