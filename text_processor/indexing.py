from text_processor.vector_store import get_vector_store

#indexing chunks to the vector store

def index_chunks(chunks):
    vector_store = get_vector_store()
    vector_store.reset_collection()
    vector_store.add_documents(chunks)
    print("Chunks have been indexed and saved to the vector store.")



















