import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def save_text_to_file(text: str, output_path: Path):
    output_path.write_text(text)

def process_pdf_folder(input_folder: Path, output_folder: Path):
    pdf_files = list(input_folder.glob("*.pdf"))
    print(pdf_files)
    output_folder.mkdir(parents=True, exist_ok=True)
    for pdf in pdf_files:
        text = extract_text_from_pdf(pdf)
        output_file = output_folder / f"{pdf.stem}.txt"
        save_text_to_file(text, output_file)