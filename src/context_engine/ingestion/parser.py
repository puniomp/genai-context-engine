from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from context_engine.schemas import Document


class DocumentParser:
    SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}

    def parse_file(self, file_path: str | Path) -> tuple[Document, str]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {suffix}")

        text = self._extract_text(path)
        if not text.strip():
            raise ValueError(f"No text extracted from file: {path}")

        document = Document(
            doc_id=self._build_doc_id(path),
            title=path.stem,
            source_path=str(path),
            content_type=suffix.lstrip("."),
            metadata={
                "filename": path.name,
                "extension": suffix,
            },
        )

        return document, text

    def _extract_text(self, path: Path) -> str:
        suffix = path.suffix.lower()

        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")

        if suffix == ".pdf":
            reader = PdfReader(str(path))
            pages: list[str] = []

            for page in reader.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)

            return "\n".join(pages)

        raise ValueError(f"Unsupported file type: {suffix}")

    def _build_doc_id(self, path: Path) -> str:
        return path.stem.lower().replace(" ", "_")
