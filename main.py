from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from admin import router as admin_router
from leads import router as leads_router
from providers import router as providers_router

app = FastAPI(title="Aqarino v2 - Dashboard")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET","aqarino-secret"))
templates = Jinja2Templates(directory="backend/app/templates")
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(leads_router, prefix="/api", tags=["leads"])
app.include_router(providers_router, prefix="/api", tags=["providers"])

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
