import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Répertoire où stocker PDFs + index
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------
# Extraction texte du PDF
# ---------------------------
def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        try:
            text += page.extract_text() or ""
        except Exception:
            continue
    return text


# ---------------------------
# Création de l’index FAISS
# ---------------------------
def index_pdf(session_id: str, pdf_path: str):
    # 1. Extraire texte
    text = extract_text_from_pdf(pdf_path)

    # 2. Découper en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_text(text)

    # 3. Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Construire l’index FAISS
    index_path = os.path.join(DATA_DIR, f"{session_id}_index")
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Sauvegarder l’index
    vectorstore.save_local(index_path)

    return index_path


# ---------------------------
# Charger un index FAISS
# ---------------------------
def load_index(session_id: str):
    index_path = os.path.join(DATA_DIR, f"{session_id}_index")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Aucun index trouvé pour session_id={session_id}")

    return FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True
    )


# ---------------------------
# Recherche vectorielle
# ---------------------------
def search_index(index, question: str, k: int = 3):
    return index.similarity_search(question, k=k)

