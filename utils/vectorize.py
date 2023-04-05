from haystack.document_stores import WeaviateDocumentStore
from haystack.schema import Document

def vectorize(data: str):
    """Vectorize text and upload to Weaviate

    Args:
        data (str): Text to vectorize

    Returns:
        None
    """
    document_store = WeaviateDocumentStore(
        host="https://vector.samiyousef.ca",
        port=443
    )
    document_store.write_documents([Document(data)])