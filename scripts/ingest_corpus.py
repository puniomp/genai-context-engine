from __future__ import annotations

from pathlib import Path

from context_engine.ingestion.chunker import TextChunker
from context_engine.ingestion.parser import DocumentParser


def main() -> None:
    raw_dir = Path("data/raw")

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_dir}")

    parser = DocumentParser()
    chunker = TextChunker(chunk_size_tokens=500, overlap_tokens=75)

    files = sorted(
        [
            path
            for path in raw_dir.iterdir()
            if path.is_file() and path.suffix.lower() in parser.SUPPORTED_EXTENSIONS
        ]
    )

    if not files:
        print("No supported documents found in data/raw")
        return

    total_docs = 0
    total_chunks = 0

    for path in files:
        document, text = parser.parse_file(path)
        chunks = chunker.chunk_document(doc_id=document.doc_id, text=text)

        total_docs += 1
        total_chunks += len(chunks)

        print(f"Document: {document.title}")
        print(f"  doc_id: {document.doc_id}")
        print(f"  content_type: {document.content_type}")
        print(f"  chunks: {len(chunks)}")

        if chunks:
            preview = chunks[0].text[:120].replace("\n", " ")
            print(f"  first_chunk_preview: {preview}...")
        print()

    print("Ingestion complete")
    print(f"Total documents: {total_docs}")
    print(f"Total chunks: {total_chunks}")


if __name__ == "__main__":
    main()
