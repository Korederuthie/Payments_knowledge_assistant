import sys

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from index_documents import (
    BASE_DIR,
    DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)


def search_documents(question, limit=3):
    load_dotenv(BASE_DIR / ".env")

    database = chromadb.PersistentClient(path=str(DB_DIR))
    collection = database.get_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
    )

    if collection.count() == 0:
        raise RuntimeError("The index is empty. Run index_documents.py.")

    api = OpenAI(timeout=60.0)
    response = api.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[question],
    )

    results = collection.query(
        query_embeddings=[response.data[0].embedding],
        n_results=min(limit, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    passages = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        passages.append({
            "text": document,
            "source": metadata["source"],
            "section": metadata["section"],
            "distance": distance,
        })

    return passages


def main():
    question = " ".join(sys.argv[1:]).strip()

    if not question:
        question = input("Enter your question: ").strip()

    if not question:
        raise SystemExit("Please enter a question.")

    print(f"\nQuestion: {question}")

    for rank, passage in enumerate(search_documents(question), start=1):
        print(f"\n--- Result {rank} ---")
        print(f"Source: {passage['source']}")
        print(f"Section: {passage['section']}")
        print(passage["text"])


if __name__ == "__main__":
    main()