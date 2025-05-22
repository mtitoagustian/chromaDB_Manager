from typing import Dict, Any, List, Optional
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient, HttpClient
from app.config import settings

class ChromaManager:
    def __init__(self):
        self.client = self._init_client()

    def _init_client(self):
        if settings.CHROMA_REMOTE_HOST:
            return HttpClient(host=settings.CHROMA_REMOTE_HOST)
        else:
            return PersistentClient(path=settings.CHROMA_IMPLEMENTATION)

    def create_collection(self, collection_name: str, metadata: Optional[dict] = None, dim: Optional[int] = None) -> str:
        try:
            collection = self.client.create_collection(
                name=collection_name,
                metadata=metadata or {"_type": "embedding"},
                embedding_function=None
            )
            return f"Collection '{collection_name}' created successfully."
        except Exception as e:
            return f"Failed to create collection '{collection_name}': {str(e)}"

    def get_collection(self, collection_name: str):
        try:
            return self.client.get_collection(name=collection_name)
        except ValueError:
            return None
        
    def delete_all_collections(self) -> str:
        try:
            collections = self.client.list_collections()
            for col in collections:
                self.client.delete_collection(name=col.name)
            return "All collections deleted successfully."
        except Exception as e:
            return f"Failed to delete collections: {str(e)}"

    def delete_collection(self, collection_name: str) -> str:
        try:
            self.client.delete_collection(name=collection_name)
            return f"Collection '{collection_name}' deleted successfully."
        except ValueError:
            return f"Collection '{collection_name}' does not exist."

    def list_collections(self) -> List[str]:
        try:
            collections = self.client.list_collections()
        
            collection_list = []
            for col in collections:
                collection_name = col.name
                metadata = col.metadata

                collection = self.client.get_collection(name=collection_name)
                data = collection.get() 

                collection_list.append({
                    "name": collection_name,
                    "metadata": metadata,
                    "document_count": len(data["ids"])
                })

            return {"collections": collection_list}

        except ValueError:
            return None


    def add_documents(
            self,
            collection_name: str,
            ids: List[str],
            documents: List[str],
            embeddings: List[List[float]],
            metadatas: Optional[List[Dict[str, Any]]] = None
        ) -> str:
        collection = self.get_collection(collection_name)
        if not collection:
            return f"Collection '{collection_name}' does not exist."

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in range(len(documents))]
        )
        return f"Documents added to collection '{collection_name}' successfully."
    
    def query_documents(
            self,
            collection_name: str,
            query_embeddings: List[List[float]],
            n_results: int = 3,
            where: Optional[Dict[str, Any]] = None
        ) -> Any:
        collection = self.get_collection(collection_name)
        if not collection:
            return f"Collection '{collection_name}' does not exist."
        
        return collection.query(query_embeddings=query_embeddings, n_results=n_results, where=where)


    def delete_embeddings(self, collection_name: str, ids: List[str]) -> str:
        collection = self.get_collection(collection_name)
        if not collection:
            return f"Collection '{collection_name}' does not exist."
        collection.delete(ids=ids)
        return f"Embeddings deleted from collection '{collection_name}'."

    def delete_embeddings_by_metadata(self, collection_name: str, metadata: Dict[str, Any]) -> str:
        collection = self.get_collection(collection_name)
        if not collection:
            return f"Collection '{collection_name}' does not exist."
        collection.delete(where=metadata)
        return f"Embeddings deleted from collection '{collection_name}' based on metadata."

    def get_collection_metadata(self, collection_name: str) -> Any:
        collection = self.get_collection(collection_name)
        if not collection:
            return f"Collection '{collection_name}' does not exist."
        return collection.get_model()
