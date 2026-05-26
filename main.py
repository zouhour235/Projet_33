from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.config import settings
from app.models.database import Base, engine
from app.api import speakers, clips, validation
from evaluation.wer_evaluator import router as wer_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Corpus de parole mooré pour la reconnaissance vocale"
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(speakers.router, prefix="/api/speakers",   tags=["Locuteurs"])
app.include_router(clips.router,    prefix="/api/clips",      tags=["Clips audio"])
app.include_router(validation.router, prefix="/api/validation", tags=["Validation"])
app.include_router(wer_router,      prefix="/api/evaluation", tags=["Évaluation WER"])

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/enregistrer", response_class=HTMLResponse)
async def enregistrer(request: Request):
    return templates.TemplateResponse(request=request, name="enregistrer.html")

@app.get("/valider", response_class=HTMLResponse)
async def valider(request: Request):
    return templates.TemplateResponse(request=request, name="valider.html")

@app.get("/health")
async def health():
    return {"statut": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)