# 🤖 Modern RAG Chatbot (QueryPilot)

A production-style **Retrieval-Augmented Generation (RAG)** chatbot built with **FastAPI, Streamlit, ChromaDB, and Sentence Transformers**, enhanced with **caching** and **web fallback search**.

---

## 🚀 Features

* 🔍 **Semantic Search (RAG)** using embeddings + vector database
* 🌐 **Web Search Fallback** (Tavily API) when no relevant docs found
* ⚡ **Query Caching (TTL-based)** for faster repeated responses
* 🧠 **LLM Integration** using Sarvam AI
* 📦 **Persistent Vector Database** (ChromaDB)
* 💬 **Clean Chat UI** using Streamlit
* 🔄 **End-to-End Pipeline** from ingestion → retrieval → generation

---

## 🏗️ Architecture Overview

```
User (Streamlit UI)
        ↓
FastAPI Backend
        ↓
     my_agent()
        ↓
 ┌───────────────┐
 │ Query Cache   │
 └──────┬────────┘
        ↓
   Retriever (RAG)
        ↓
Vector DB (ChromaDB)
        ↓
  Docs Found?
   /     \
 YES      NO
 ↓         ↓
Context   Web Search (Tavily)
   \       /
    ↓     ↓
     LLM (Sarvam)
        ↓
   Final Response
```

---

## 📂 Project Structure

```
work_space/
│
├── agent.py              # Core logic (RAG + cache + LLM)
├── retriever.py          # Retrieval logic
├── vector_db.py          # ChromaDB integration
├── embedding_manager.py  # Embedding generation
├── data_ingestion.py     # Load + split documents
│
server/
├── backend.py            # FastAPI server
├── app.py                # Streamlit UI
│
fetched_data/
└── text_docs/            # Stored documents & web results
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd <your-project>
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
SARVAM_API_KEY=your_sarvam_key
TAVILY_API_KEY=your_tavily_key
```

---

## ▶️ Running the Project

### 1. Start Backend (FastAPI)

```bash
cd backend
python backend.py
```

Server runs at:

```
http://127.0.0.1:8000
```

---

### 2. Start Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

---

## 🔄 How It Works

### 1. Data Ingestion

* Loads `.txt` files
* Splits into chunks
* Converts into embeddings
* Stores in ChromaDB

---

### 2. Query Flow

1. User sends query
2. Query cache checked
3. Retriever searches vector DB
4. If no results → web search
5. Context passed to LLM
6. Response generated
7. Stored in cache

---

## 🧠 Caching System

| Cache Type  | Purpose                  | TTL        |
| ----------- | ------------------------ | ---------- |
| Query Cache | Avoid repeated LLM calls | 1 hour     |
| Web Cache   | Avoid repeated API calls | 30 minutes |

---

## 📌 Key Technologies

* **FastAPI** → Backend API
* **Streamlit** → UI
* **ChromaDB** → Vector storage
* **Sentence Transformers** → Embeddings
* **Sarvam AI** → LLM
* **Tavily API** → Web search

---

## ⚡ Future Improvements

* 🔥 Add **reranker (cross-encoder)**
* 🧠 Implement **chat memory (context-aware RAG)**
* ⚡ Use **Redis for caching**
* 📊 Add **observability (logs + metrics)**
* 🔀 Hybrid search (keyword + semantic)
* 🧩 Multi-agent system

---

## 🧑‍💻 Author

Built with 💡 by an AI engineer on a mission to create intelligent systems.

---

## ⭐ Final Note

This is not just a chatbot —
it’s a **mini AI system architecture** combining:

* Retrieval
* Reasoning
* External knowledge
* Performance optimization

---

If you’re building on top of this, you’re already thinking like a **real AI engineer** 🚀
