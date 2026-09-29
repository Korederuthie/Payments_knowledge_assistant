from pathlib import Path
import os
import re

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
DB_DIR = BASE_DIR / ".chroma"

EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "payments_knowledge"


def load_sections():
    """Create one searchable passage per Markdown section."""
    passages = []

    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parts = re.split(r"(?m)^## ", text)

        # Preserve the title, document ID and version in every passage.
        document_header = parts[0].strip()

        for number, section in enumerate(parts[1:], start=1):
            heading, _, body = section.partition("\n")

            if not body.strip():
                continue

            passages.append({
                "id": f"{path.name}::section-{number}",
                "text": (
                    f"{document_header}\n\n"
                    f"## {heading.strip()}\n{body.strip()}"
                ),
                "metadata": {
                    "source": path.name,
                    "section": heading.strip(),
                },
            })

    return passages


def main():
    load_dotenv(BASE_DIR / ".env")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    passages = load_sections()

    if not passages:
        raise RuntimeError("No Markdown sections found in docs.")

    print(f"Found {len(passages)} document sections.")
    print("Generating embeddings...")

    api = OpenAI(timeout=60.0)

    response = api.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[passage["text"] for passage in passages],
    )

    # Match returned embeddings to the original input order.
    embeddings = [
        item.embedding
        for item in sorted(response.data, key=lambda item: item.index)
    ]

    database = chromadb.PersistentClient(path=str(DB_DIR))
    collection = database.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
    )

    collection.upsert(
        ids=[passage["id"] for passage in passages],
        documents=[passage["text"] for passage in passages],
        metadatas=[passage["metadata"] for passage in passages],
        embeddings=embeddings,
    )

    # Remove outdated passages when documents change.
    current_ids = {passage["id"] for passage in passages}
    stored_ids = set(collection.get()["ids"])
    obsolete_ids = stored_ids - current_ids

    if obsolete_ids:
        collection.delete(ids=list(obsolete_ids))

    print(f"Indexed {collection.count()} sections successfully.")
    print(f"Local database: {DB_DIR}")


if __name__ == "__main__":
    main()