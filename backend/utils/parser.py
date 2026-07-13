import pypdf
import docx2txt

# PDF file se text nikalne ke liye function
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Word (.docx) file se text nikalne ke liye function
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Main function jo check karega ki file PDF hai ya Word
def parse_resume(file_path, file_extension):
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Sirf PDF ya DOCX file hi allowed hai!")