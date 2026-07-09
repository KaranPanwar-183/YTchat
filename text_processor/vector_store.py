import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

_embeddings = None
_vector_store = None

def get_vector_store():

    global _vector_store, _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            encode_kwargs={"normalize_embeddings": True},
        )

    if _vector_store is None:
        _vector_store = Chroma(
            collection_name="youtube_transcripts",
            embedding_function=_embeddings,
            persist_directory="./chroma_db"
        )

    return _vector_store



