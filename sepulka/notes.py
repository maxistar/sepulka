from pathlib import Path
import re


NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"


def _keywords(query: str) -> set[str]:
    return {word.lower() for word in re.findall(r"[\wа-яА-ЯёЁ]+", query) if len(word) >= 3}


def read_notes(query: str, notes_dir: Path = NOTES_DIR) -> list[dict[str, str]]:
    """Search markdown notes with simple keyword matching."""

    notes_dir.mkdir(parents=True, exist_ok=True)
    query_words = _keywords(query)
    matches = []

    for path in sorted(notes_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        haystack = f"{path.stem} {content}".lower()
        score = sum(1 for word in query_words if word in haystack)
        if score:
            matches.append({"title": path.stem, "path": str(path), "content": content, "score": str(score)})

    matches.sort(key=lambda item: int(item["score"]), reverse=True)
    return matches[:5]


def write_note(title: str, content: str, notes_dir: Path = NOTES_DIR) -> Path:
    """Write a markdown note under notes/ using a safe filename."""

    notes_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ_-]+", "-", title.strip().lower()).strip("-")
    if not slug:
        slug = "untitled"

    path = notes_dir / f"{slug}.md"
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path
