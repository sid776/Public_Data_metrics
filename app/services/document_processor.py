"""Document ingestion: PDF text extraction and chunking for RAG."""
from pathlib import Path
from typing import List, Tuple

from config.settings import settings


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """Split text into overlapping chunks (by characters)."""
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap
    if not text or not text.strip():
        return []
    text = text.replace("\r\n", "\n").strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_break = max(
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind(" "),
            )
            if last_break > chunk_size // 2:
                chunk = chunk[: last_break + 1]
                end = start + last_break + 1
        chunks.append(chunk.strip())
        start = end - overlap
    return [c for c in chunks if c]


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract raw text from a PDF file."""
    import PyPDF2
    text_parts = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return "\n\n".join(text_parts)


def extract_text_from_txt(file_path: Path) -> str:
    """Read plain text file."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_and_chunk_file(file_path: Path) -> Tuple[List[str], List[dict]]:
    """Load a file (PDF or TXT), chunk it, return chunks and metadatas."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        raw = extract_text_from_pdf(path)
    elif suffix in (".txt", ".md"):
        raw = extract_text_from_txt(path)
    else:
        raise ValueError(f"Unsupported format: {suffix}. Use .pdf, .txt, or .md")
    chunks = chunk_text(raw)
    source = path.name
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
    return chunks, metadatas


class DocumentProcessor:
    """Orchestrate file loading, chunking, and optional vector store ingestion."""

    @staticmethod
    def process_file(file_path: Path) -> Tuple[List[str], List[dict]]:
        """Process a single file into chunks and metadatas."""
        return load_and_chunk_file(Path(file_path))

    @staticmethod
    def process_directory(dir_path: Path) -> Tuple[List[str], List[dict]]:
        """Process all supported files in a directory."""
        all_chunks = []
        all_metadatas = []
        for ext in ("*.pdf", "*.txt", "*.md"):
            for f in Path(dir_path).rglob(ext):
                try:
                    chunks, metas = load_and_chunk_file(f)
                    all_chunks.extend(chunks)
                    all_metadatas.extend(metas)
                except Exception:
                    continue
        return all_chunks, all_metadatas
