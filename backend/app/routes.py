import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from .rag import index_pdf, load_index, search_index
from .llm import MistralClient

router = APIRouter()
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------
# Upload d'un PDF
# ---------------------------
@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), session_id: str = Form(None)):
    try:
        # Générer un session_id si pas fourni
        sid = session_id or str(uuid.uuid4())

        # Sauvegarder le PDF brut
        pdf_path = os.path.join(DATA_DIR, f"{sid}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Construire un index FAISS
        index_path = index_pdf(sid, pdf_path)

        return {
            "session_id": sid,
            "filename": file.filename,
            "index_path": index_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Query (poser une question)
# ---------------------------
class QueryRequest(BaseModel):
    session_id: str
    question: str


@router.post("/query")
async def query(req: QueryRequest):
    try:
        # 1. Charger l’index FAISS
        index = load_index(req.session_id)

        # 2. Passages les plus proches
        docs = search_index(index, req.question)
        context = "\n\n".join([d.page_content for d in docs])

        # 3. Construire le prompt
        prompt = (
            "Réponds à la question en utilisant uniquement le contexte suivant. "
            "Si la réponse n’est pas dans le contexte, dis que tu ne sais pas.\n\n"
            f"Contexte:\n{context}\n\n"
            f"Question: {req.question}\nRéponse:"
        )

        # 4. Appeler Mistral
        client = MistralClient()
        answer = client.generate(prompt)

        return {
            "session_id": req.session_id,
            "question": req.question,
            "answer": answer.strip(),
            "sources": [
                {"content": d.page_content[:200], "metadata": d.metadata}
                for d in docs
            ],
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Aucun index trouvé pour ce session_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


