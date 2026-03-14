from context_engine.ingestion.chunker import TextChunker


def test_chunk_document_returns_chunks():
    text = "This is a sample sentence. " * 300
    chunker = TextChunker(chunk_size_tokens=100, overlap_tokens=20)

    chunks = chunker.chunk_document(doc_id="doc-1", text=text)

    assert len(chunks) > 1
    assert chunks[0].doc_id == "doc-1"
    assert chunks[0].chunk_index == 0
    assert chunks[0].token_count <= 100


def test_empty_text_returns_no_chunks():
    chunker = TextChunker()
    chunks = chunker.chunk_document(doc_id="doc-1", text="   ")

    assert chunks == []
