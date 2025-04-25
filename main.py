from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

import os


app = FastAPI(
    title="Text Humanizer",
    description="Преобразует текст в более естественный человеческий вариант"
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static")