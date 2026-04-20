import os
from typing import List, Dict
from config.company_structure import get_accessible_departments

BASE_DOC_PATH = "data"

documents_store: List[Dict] = []


def load_documents():
    global documents_store
    documents_store = []

    for department in os.listdir(BASE_DOC_PATH):
        department_path = os.path.join(BASE_DOC_PATH, department)

        if not os.path.isdir(department_path):
            continue

        for file in os.listdir(department_path):
            file_path = os.path.join(department_path, file)

            if file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                doc = {
                    "id": f"{department}_{file}",
                    "department": department,
                    "filename": file,
                    "content": content
                }

                documents_store.append(doc)

    print(f"Loaded {len(documents_store)} documents.")


def get_all_documents():
    return documents_store