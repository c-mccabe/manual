from pathlib import Path
from src.ingestion import process_pdf_folder
from src.chunking import chunk_text
from src.embedding import embed_chunks
from dotenv import load_dotenv


load_dotenv()

if __name__ == "__main__":
    raw_pdfs = Path("/Users/Conor/src/manual/data/raw_pdfs/")
    processed_texts = Path("/Users/Conor/src/manual/data/processed_texts")

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