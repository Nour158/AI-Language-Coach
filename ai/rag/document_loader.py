from pathlib import Path

import pandas as pd
from pypdf import PdfReader


class KnowledgeDocumentLoader:
    def __init__(self, knowledge_dir):
        self.knowledge_dir = Path(knowledge_dir)

    def load_pdf(self, file_path):
        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                pages.append({
                    "text": text.strip(),
                    "metadata": {
                        "source": str(file_path),
                        "page": page_number,
                        "file_type": "pdf"
                    }
                })

        return pages

    def load_tsv(self, file_path):
        df = pd.read_csv(file_path, sep="\t")

        records = []

        for index, row in df.iterrows():
            text = " | ".join(
                f"{column}: {value}"
                for column, value in row.items()
                if pd.notna(value)
            )

            records.append({
                "text": text,
                "metadata": {
                    "source": str(file_path),
                    "row": index,
                    "file_type": "tsv"
                }
            })

        return records

    def load_file(self, file_path):
        file_path = Path(file_path)

        if file_path.suffix.lower() == ".pdf":
            return self.load_pdf(file_path)

        elif file_path.suffix.lower() == ".tsv":
            return self.load_tsv(file_path)

        else:
            print(f"Unsupported file type: {file_path}")
            return []

    def load_all(self):
        documents = []

        for file_path in self.knowledge_dir.rglob("*"):
            if file_path.is_file():
                documents.extend(self.load_file(file_path))

        return documents