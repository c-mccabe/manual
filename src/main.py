from pathlib import Path
from ingestion import process_pdf_folder
from chunking import chunk_text
from embedding import embed_chunks
from query import query_manual

if __name__ == "__main__":
    raw_pdfs = Path("data/raw_pdfs")
    processed_texts = Path("data/processed_texts")

    print("Extracting text from PDFs...")
    process_pdf_folder(raw_pdfs, processed_texts)

    all_chunks = []
    for txt_file in processed_texts.glob("*.txt"):
        text = txt_file.read_text()
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    print("Embedding chunks...")
    embed_chunks(all_chunks, persist_directory="./chroma_store")

    print("Ready to query! Try an example:")
    response = query_manual("The screen won't turn on - what should I do?", persist_directory="./chroma_store")
    print(response)