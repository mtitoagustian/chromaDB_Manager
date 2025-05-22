from pathlib import Path

class Settings:
    #global settings
    CHROMA_REMOTE_HOST = None
    CHROMA_DOCUMENT_COLLECTION = Path("documents_collection")
    CHROMA_IMPLEMENTATION = ".chromadb"
    EMBEDDING_DIMENSION = 384
    
settings = Settings()