from context_engine.ingestion.parser import DocumentParser


def test_parse_txt_file():
    parser = DocumentParser()

    doc, text = parser.parse_file("data/raw/sample_policy.txt")

    assert doc.doc_id == "sample_policy"
    assert doc.title == "sample_policy"
    assert doc.content_type == "txt"
    assert "responsible development" in text.lower()
