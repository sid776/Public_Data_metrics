"""Ingest sample_docs into the vector store. Run from project root: python scripts/ingest_sample_docs.py"""
import sys
from pathlib import Path

# Ensure project root is on path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app.core.vector_store import VectorStore
from app.services.document_processor import DocumentProcessor


def main():
    sample_dir = project_root / "sample_docs"
    if not sample_dir.is_dir():
        print("sample_docs/ not found. Create it and add PDF or TXT files.")
        return
    chunks, metadatas = DocumentProcessor.process_directory(sample_dir)
    if not chunks:
        print("No supported files (.pdf, .txt, .md) in sample_docs/.")
        return
    store = VectorStore()
    store.add_documents(chunks, metadatas=metadatas)
    print(f"Ingested {len(chunks)} chunks from {sample_dir}.")


if __name__ == "__main__":
    main()
