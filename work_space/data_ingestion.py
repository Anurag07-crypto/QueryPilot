# //////////////////////////////////////////////
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredFileLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
# //////////////////////////////////////////////
# Use absolute path based on script location for reliable loading
def load_documents():
    path = Path(__file__).parent.parent / "fetched_data" / "text_docs"
    Dir_loader = DirectoryLoader(
    path=path,
    glob="**/*.txt",
    loader_cls=UnstructuredFileLoader
)
    return Dir_loader.load()

# //////////////////////////////////////////////
def splitter(documents, chunk_size:int = 1000, chunk_overlap:int = 200):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n","\n\n",""]
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs
# //////////////////////////////////////////////
