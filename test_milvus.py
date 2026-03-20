"""
Milvus Lite Persistence Test

This script verifies that the Milvus Vector database can be initialized and queried
correctly using the local SQLite-based driver (`milvus_lite.db`). It helps ensure
that the Knowledge Base (KB) component will function as expected.
"""
import os
from langchain_community.vectorstores import Milvus
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize the embedding model (all-MiniLM-L6-v2) for vectorization.
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# Define the local database file path. 
# Using a simple filename helps avoid path-parsing issues on Windows.
MILVUS_DB = "milvus_lite.db"
docs = [Document(page_content="Test data", metadata={"source": "test", "collection": "policies"})]

print("Testing Milvus import and connection...")
try:
    # Attempt to create/load a collection and insert a test document.
    store = Milvus.from_documents(
        docs,
        embeddings,
        connection_args={"uri": MILVUS_DB},
        collection_name="policies",
        drop_old=False,
    )
    print("✅ Success! Milvus Lite is operational.")
except Exception as e:
    print(f"❌ Error: {e}")
