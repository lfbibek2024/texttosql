# Retrieves schema and example queries from local ChromaDB

import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def get_schema_context(db_id, nl_query):
    # Connect to local ChromaDB
    client = chromadb.Client(Settings())
    # Use OpenAI embedding function (or default if not available)
    try:
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )
    except Exception:
        openai_ef = None
    
    # Get or create collection for the database
    collection = client.get_or_create_collection(
        name=db_id,
        embedding_function=openai_ef
    )
    # Embed the NL query and query ChromaDB for relevant schema/examples
    results = collection.query(
        query_texts=[nl_query],
        n_results=3
    )
    # Combine retrieved documents as context
    docs = results.get('documents', [[]])[0]
    context = '\n'.join(docs) if docs else ""
    return context
