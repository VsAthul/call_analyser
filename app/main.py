from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.models import Call
from app.models import Transcript
from app.models import Summary
from app.models import QAHistory
from app.models import AudioSummary
from app.core.database import Base
from app.core.database import engine
# from app.models import *
from app.api.routes.upload import router as upload_router
from app.api.routes.transcript import router as transcript_router
from app.api.routes.summary import router as summary_router
from app.api.routes.qa import router as qa_router
from app.api.routes.audio_summary import router as audio_summary_router
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.api.routes.summary_list import router as summary_list_router


Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Banking Call Analyzer",
    version="1.0.0"
)
templates = Jinja2Templates(
    directory="templates"
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/generated_audio",
    StaticFiles(
        directory="generated_audio"
    ),
    name="generated_audio"
)

app.include_router(upload_router)
app.include_router(transcript_router)
app.include_router(summary_router)
app.include_router(summary_list_router)
app.include_router(qa_router)
# app.include_router(audio_summary_router)


@app.get("/")
async def home(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )