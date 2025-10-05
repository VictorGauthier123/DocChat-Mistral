# DocChat Mistral

DocChat Mistral is a full-stack web application that allows users to ask questions about a PDF document using a Mistral LLM and a Retrieval-Augmented Generation (RAG) pipeline with FAISS.


## Screenshot

Exemple with my CV : 


## Objective

This project demonstrates how to combine:
- A modern **frontend** with **Next.js** and **TypeScript**
- A robust **backend** using **FastAPI** (Python)
- A **Large Language Model (LLM)** for intelligent document reasoning
- A **vector database** (**FAISS**) for contextual search
- An orchestrator layer with **LangChain**

## Architecture

```
docchat-mistral/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── routes.py        # Upload and query endpoints
│   │   ├── rag.py           # RAG logic (embeddings + FAISS search)
│   │   ├── llm.py           # Mistral model integration
│   │   └── utils.py         # PDF parsing and text processing
│   ├── requirements.txt     # Backend dependencies
│   └── .env                 # Environment variables (Mistral API key)
│
├── frontend/
│   ├── src/
│   │   ├── app/page.tsx     # Main page (upload + chat)
│   │   └── components/
│   │       └── ChatUI.tsx   # Chat interface
│   ├── package.json
│   └── tsconfig.json
│
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/VictorGauthier123/docchat-mistral.git
cd docchat-mistral
```

### 2. Backend setup

Create and activate a virtual environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create an `.env` file:
```bash
MISTRAL_API_KEY=your_mistral_api_key_here
```

Run the backend server:
```bash
uvicorn app.main:app --reload
```

The backend will be available at **http://localhost:8000**.

### 3. Frontend setup

```bash
cd ../frontend
npm install
```

Create a `.env.local` file:
```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

Run the development server:
```bash
npm run dev
```

The frontend will be available at **http://localhost:3000**.

## Features

| Feature | Description |
|----------|-------------|
| PDF Upload | Upload a local PDF document |
| Text Extraction | Extracts text from the uploaded PDF using PyMuPDF |
| FAISS Indexing | Encodes text chunks into embeddings and stores them in FAISS |
| Intelligent Chat | Sends user questions and retrieves context-aware answers from the Mistral model |
| RAG Pipeline | Combines vector search and LLM reasoning for accurate responses |
| Modern UI | Clean, responsive chat interface inspired by ChatGPT |

## Main Dependencies

### Backend
- FastAPI
- LangChain
- FAISS
- SentenceTransformers
- PyMuPDF
- python-dotenv

### Frontend
- Next.js 15
- TypeScript
- TailwindCSS
- Axios
- React Hooks

## Usage

1. Start the backend: `uvicorn app.main:app --reload`
2. Start the frontend: `npm run dev`
3. Open [http://localhost:3000](http://localhost:3000)
4. Upload a PDF and ask questions about its content

## How it works

1. The PDF is converted into raw text.
2. The text is split into smaller chunks.
3. Each chunk is transformed into embeddings using `sentence-transformers`.
4. The vectors are stored in FAISS for semantic retrieval.
5. When a question is asked:
   - FAISS retrieves the most relevant passages.
   - LangChain composes the context and query.
   - The **Mistral** model generates a context-aware answer.


