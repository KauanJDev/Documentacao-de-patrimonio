from fastapi import FastAPI
from routes.documentos import router as documentos_router
from routes.backup import router as backups_router
from routes.exportar import router as exportar_router

app = FastAPI()

app.include_router(documentos_router)
app.include_router(backups_router)
app.include_router(exportar_router)
