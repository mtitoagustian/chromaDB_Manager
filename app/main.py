from fastapi import FastAPI
from app.middlewares.response_wrapper import ResponseWrapperMiddleware, register_exception_handlers
from app.public_api.chroma_router import router as chroma_router
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "ChromaDB API"
app.description = "API untuk mengelola koleksi dan dokumen di ChromaDB."
app.version = "1.0.0"

#app.add_middleware(ResponseWrapperMiddleware)
#register_exception_handlers(app)
app.include_router(chroma_router)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    html_content = """
    <html>
        <head>
            <meta http-equiv="refresh" content="3;url=/docs" />
            <title>Administrator HC Chatbot</title>
        </head>
        <body>
            <h1>Selamat Datang di Administrator HC Chatbot!</h1>
            <p>Anda akan diarahkan ke dokumentasi API dalam 3 detik...</p>
            <p>Jika tidak, klik <a href="/docs">di sini</a>.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
