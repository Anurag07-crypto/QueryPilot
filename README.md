# 🤖 Modern RAG Chatbot — QueryPilot

A production-grade **Retrieval-Augmented Generation (RAG)** system built with **FastAPI, Streamlit, ChromaDB, and Sentence Transformers**, enhanced with **query rewriting, intelligent caching, logging, testing, and robust error handling**.

This project is designed as a **real-world AI system**, focusing not only on accuracy but also on **scalability, maintainability, and reliability**.

---

## 🚀 Key Features

### 🧠 Core Intelligence

* 🔍 **Semantic Search (RAG)** using embeddings + ChromaDB
* ✍️ **Query Rewriting Layer** → improves retrieval quality
* 🌐 **Web Search Fallback (Tavily API)**
* 🤖 **LLM Integration (Sarvam AI)**

---

### ⚡ Performance Optimization

* ⚡ **TTL-Based Query Caching**
* 🌐 **Web Cache** for API efficiency
* 🧩 Optimized pipeline to reduce latency

---

### 🏗️ Software Engineering Enhancements (NEW 🔥)

* 🧼 **Clean Code Structure**

  * Modular design (`agent`, `retriever`, `vector_db`, etc.)
  * Separation of concerns across layers
  * Maintainable and extensible architecture

* 🪵 **Logging System**

  * Centralized logging module (`logger.py`)
  * Tracks pipeline flow, errors, and debugging info
  * Helps in monitoring and debugging production issues

* 🧪 **Testing Suite (Pytest)**

  * Unit tests for:

    * Backend API
    * Embedding Manager
    * Vector DB
  * Ensures system reliability and prevents regressions

* ⚠️ **Robust Error Handling**

  * Graceful failure handling across pipeline
  * API-level exception handling
  * Prevents system crashes and improves user experience

---

## 🏗️ Architecture Overview

```id="flow123"
User (Streamlit UI)
        ↓
FastAPI Backend (/chat)
        ↓
    Query Rewriting
        ↓
     my_agent()
        ↓
 ┌───────────────────────┐
 │   Query Cache (TTL)   │
 └──────────┬────────────┘
            ↓
      Retriever (RAG)
            ↓
     Vector DB (ChromaDB)
            ↓
       Docs Found?
        /     \
      YES      NO
       ↓        ↓
   Context   Web Search (Tavily)
       \        /
        ↓      ↓
     LLM (Sarvam AI)
            ↓
     Final Response
            ↓
        Logging + Cache
```

---

## 📂 Project Structure

```id="projx99"
root/
│
├── work_space/
│   ├── agent.py
│   ├── retriever.py
│   ├── vector_db.py
│   ├── embedding_manager.py
│   ├── data_ingestion.py
│   ├── logger.py              # Logging system
│
├── server/
│   ├── backend.py             # FastAPI API
│   ├── app.py                 # Streamlit UI
│
├── tests/
│   ├── test_backend.py
│   ├── test_embedding_manager.py
│   ├── test_vector_db.py
│
├── fetched_data/              # Stored docs + web results
├── logs/                      # Log files
├── .env
├── README.md
```

---

## ⚙️ Installation

```bash id="ins1"
git clone <your-repo-url>
cd <your-project>
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

```
SARVAM_API_KEY=your_key
TAVILY_API_KEY=your_key
```

---

## ▶️ Running the Project

### Backend

```bash id="run1"
cd server
python backend.py
```

### Frontend

```bash id="run2"
streamlit run app.py
```

---

## 🧪 Running Tests

```bash id="test1"
pytest tests/
```

---

## 🧠 Caching System

| Cache Type  | Purpose                  | TTL        |
| ----------- | ------------------------ | ---------- |
| Query Cache | Avoid repeated LLM calls | 1 hour     |
| Web Cache   | Avoid repeated API calls | 30 minutes |

---

## 📌 Tech Stack

* FastAPI
* Streamlit
* ChromaDB
* Sentence Transformers
* Sarvam AI
* Tavily API
* Pytest

---

## ⚡ Future Improvements

* 🔥 Cross-Encoder Reranker
* 🧠 Conversational Memory
* ⚡ Redis Caching
* 📊 Observability (Prometheus + Grafana)
* 🔀 Hybrid Search (BM25 + Semantic)
* 🧩 Multi-Agent System

---

## 🧑‍💻 Author

Built with 💡 by an AI engineer focused on **real-world system design + intelligent applications**.

---

## ⭐ Final Note

This is not just a chatbot —
it’s a **production-style AI system** combining:

* Retrieval
* Query Optimization
* Fault Tolerance
* Testing
* Logging
* Performance Engineering

---

If you're building systems like this, you're already thinking beyond tutorials —
you're thinking like an **AI systems engineer** 🚀
