# from typing import Any, Dict, List, Optional

# import chromadb

# client = chromadb.PersistentClient(path="../../local_data_store/chroma_db")


# collection_name = "documents"


# collection = client.get_or_create_collection(collection_name)


# def add_document_chunks(
#     document_id: str, chunks: List[str], metadata: Dict[str, Any], org_id: str
# ):
#     """Add document chunks to vector store"""
#     if not chunks:
#         return

#     chunk_ids = []
#     chunk_metadatas = []

#     for i, _ in enumerate(chunks):
#         chunk_id = f"{document_id}_chunk_{i}"
#         chunk_metadata = {
#             **metadata,
#             "document_id": document_id,
#             "chunk_index": i,
#             "org_id": org_id,
#         }
#         chunk_ids.append(chunk_id)
#         chunk_metadatas.append(chunk_metadata)

#     collection.add(documents=chunks, metadatas=chunk_metadatas, ids=chunk_ids)


# def search_documents(
#     query: str,
#     org_id: str,
#     n_results: int = 10,
#     filter_metadata: Optional[Dict[str, Any]] = None,
# ) -> List[Dict[str, Any]]:
#     """Search similar documents by query"""
#     where_clause = {"org_id": org_id}
#     if filter_metadata:
#         where_clause.update(filter_metadata)

#     results = collection.query(
#         query_texts=[query],
#         n_results=n_results,
#         where=where_clause,
#         include=["documents", "distances", "metadatas"],
#     )

#     return [
#         {"document": doc, "metadata": meta, "distance": dist, "chunk_id": chunk_id}
#         for doc, meta, dist, chunk_id in zip(
#             results["documents"][0],
#             results["metadatas"][0],
#             results["distances"][0],
#             results["ids"][0],
#         )
#     ]
