from .vector_store import get_vector_store


def get_retriever():
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 20,
            "lambda_mult": 0.5,
        },
    )