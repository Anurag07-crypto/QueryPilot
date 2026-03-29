from .data_ingestion import splitter
from .vector_db import VectorStore
from .embedding_manager import Embedding_manager
from .retriever import Retriever
from sarvamai import SarvamAI
import os
from langchain_tavily import TavilySearch
from langchain_exa import ExaSearchResults
from dotenv import load_dotenv
import uuid
import time
from pathlib import Path
from .data_ingestion import load_documents
# ////////////////////////////////////////////////////////////////////////
QUERY_TTL = 3600        # 1 hour
WEB_TTL = 1800          # 30 minutes
# ////////////////////////////////////////////////////////////////////////
load_dotenv(Path(__file__).parent / ".env")
sarvam_api_key=os.getenv("SARVAM_API_KEY")
tavily_api_key=os.getenv("TAVILY_API_KEY")

if not sarvam_api_key or not tavily_api_key :
    raise ValueError("API_KEY environment variable is not set")

# ////////////////////////////////////////////////////////////////////
client = SarvamAI(api_subscription_key=sarvam_api_key)
tavily = TavilySearch(max_results=5)
exa = ExaSearchResults()
# ////////////////////////////////////////////////////////////////////////
embedding_manager = Embedding_manager()
vector_store = VectorStore()
# ////////////////////////////////////////////////////////////////////////
WEB_CACHE = {}
def web_search(query):
    if query in WEB_CACHE:
        if is_valid(WEB_CACHE[query], WEB_TTL):
            print("WEB CACHE HIT")
            return WEB_CACHE[query]["answer"]
        else:
            print("QUERY CACHE OUTDATED")
            del WEB_CACHE[query]

    tavily_result = tavily.invoke(query)
    tavily_text = "\n\n".join([r["content"] for r in tavily_result["results"]]) if tavily_result.get("results") else ""
    WEB_CACHE[query] = {
        "answer":tavily_text,
        "time_stamp":time.time()
        }
    # Use absolute paths relative to this file
    docs_dir = Path(__file__).parent.parent / "fetched_data" / "text_docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    tavily_path = docs_dir / f"tavily_results_{uuid.uuid4()}.txt"
    with open(tavily_path, "w", encoding="utf-8") as f:
        f.write(tavily_text)
    return tavily_text
# ////////////////////////////////////////////////////////////////////////
DATA_LOADED = False
def initialize_loader():
    
    global DATA_LOADED
    if DATA_LOADED:
        return
    
    documents = load_documents()
    chunks = splitter(documents)
    texts = [doc.page_content for doc in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)
    vector_store.add_documents(chunks,embeddings)
    
    DATA_LOADED = True

retriever = initialize_loader()

retriever = Retriever(embedding_manager, vector_store)
# ------------------------------------------------------------------------
def is_valid(cache_entry, ttl):
    return (time.time() - cache_entry["time_stamp"]) < ttl

# ------------------------------------------------------------------------
QUERY_CACHE = {}

def my_agent(query,client=client):
    
    if query in QUERY_CACHE:
        if is_valid(QUERY_CACHE[query], QUERY_TTL):
            print("QUERY CACHE HIT")
            return QUERY_CACHE[query]["answer"]
        else:
            print("QUERY CACHE OUTDATED")
            del QUERY_CACHE[query]
    
    context = retriever.retrieve(query=query)
    if not context:
        web_context = web_search(query=query)
        context = web_context
    context_text = "\n\n".join([doc["content"] for doc in context]) if isinstance(context, list) else str(context)
    prompt = f"""
You are an AI assistant.

IMPORTANT:
- Do NOT include reasoning steps
- Do NOT explain your thinking
- ONLY return final answer

Context:
{context_text}

Question:
{query}
"""
    
    response = client.chat.completions(
            model="sarvam-105b",
            messages=[
                {"role":"user",
                 "content":prompt}
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1000,
        )

    msg = response.choices[0].message

    final_answer = msg.content or msg.reasoning_content
    QUERY_CACHE[query] = {
        "answer":final_answer,
        "time_stamp":time.time()
        }
  
    if "Analyze the User's Request" in final_answer:
        final_answer = final_answer.split("Final Answer:")[-1]

    return final_answer.strip()


# ////////////////////////////////////////////////////////////////////
