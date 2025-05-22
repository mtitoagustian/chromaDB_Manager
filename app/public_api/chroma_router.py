from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.chroma_manager import ChromaManager

router = APIRouter(prefix="/chroma", tags=["ChromaDB"])
chroma = ChromaManager()

# ======== REQUEST SCHEMAS ========
class CreateCollectionRequest(BaseModel):
    collection_name: str
    metadata: Optional[Dict[str, Any]] = None
    dim: Optional[int] = None

class AddDocumentsRequest(BaseModel):
    collection_name: str
    ids: List[str]
    documents: List[str]
    embeddings: List[List[float]]
    metadatas: Optional[List[Dict[str, Any]]] = None

class QueryDocumentsRequest(BaseModel):
    collection_name: str
    query_embeddings: List[List[float]]
    n_results: int = 3
    where: Optional[Dict[str, Any]] = None

class DeleteEmbeddingsRequest(BaseModel):
    collection_name: str
    ids: List[str]

class DeleteEmbeddingsByMetadataRequest(BaseModel):
    collection_name: str
    metadata: Dict[str, Any]

# ======== ENDPOINTS ========
@router.post("/create")
def create_collection(req: CreateCollectionRequest):
    try:
        result = chroma.create_collection(req.collection_name, req.metadata, req.dim)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get")
def get_collection(collection_name: str):
    try:
        collection = chroma.get_collection(collection_name)
        if not collection:
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found.")
        return collection.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
def delete_collection(collection_name: str):
    try:
        result = chroma.delete_collection(collection_name)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
def list_collections():
    try:
        return {"collections": chroma.list_collections()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-documents")
def add_documents(req: AddDocumentsRequest):
    try:
        result = chroma.add_documents(
            collection_name=req.collection_name,
            ids=req.ids,
            documents=req.documents,
            embeddings=req.embeddings,
            metadatas=req.metadatas
        )
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
def query_documents(req: QueryDocumentsRequest):
    try:
        result = chroma.query_documents(
            collection_name=req.collection_name,
            query_embeddings=req.query_embeddings,
            n_results=req.n_results,
            where=req.where
        )
        if isinstance(result, str):
            raise HTTPException(status_code=404, detail=result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-embeddings")
def delete_embeddings(req: DeleteEmbeddingsRequest):
    try:
        result = chroma.delete_embeddings(req.collection_name, req.ids)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-embeddings-by-metadata")
def delete_embeddings_by_metadata(req: DeleteEmbeddingsByMetadataRequest):
    try:
        result = chroma.delete_embeddings_by_metadata(req.collection_name, req.metadata)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metadata")
def get_collection_metadata(collection_name: str):
    try:
        result = chroma.get_collection_metadata(collection_name)
        if isinstance(result, str):
            raise HTTPException(status_code=404, detail=result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-all-collection")
def delete_all_collections():
    try:
        result = chroma.delete_all_collections()
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))