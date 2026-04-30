import PyPDF2


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)


def clean_text(text):
    return " ".join((text or "").split())


def split_blocks(text, min_length=40):
    blocks = []
    current = []
    current_length = 0

    for line in (text or "").splitlines():
        cleaned = clean_text(line)
        if not cleaned:
            continue

        current.append(cleaned)
        current_length += len(cleaned)

        if current_length >= 240:
            blocks.append(" ".join(current))
            current = []
            current_length = 0

    if current:
        blocks.append(" ".join(current))

    return [block for block in blocks if len(block) >= min_length] or [clean_text(text)]


def split_statements(text, min_length=35):
    normalized = clean_text(text)
    for marker in ["•", " - ", ";", ". ", "? ", "! "]:
        normalized = normalized.replace(marker, "\n")

    return [
        item.strip()
        for item in normalized.splitlines()
        if len(item.strip()) >= min_length
    ]
