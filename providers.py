from fastapi import APIRouter
import os, httpx
router = APIRouter()

@router.get("/detect")
async def detect():
    providers = {"ollama": False, "local": False, "openai": False, "anthropic": False}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:11434/api/status", timeout=1.5)
            if r.status_code == 200: providers["ollama"] = True
    except: pass
    local_url = os.getenv("LOCAL_LLM_URL", "http://localhost:8080/v1/chat/completions")
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(local_url.replace("/v1/chat/completions","/healthz"), timeout=1.5)
            if r.status_code in (200,204): providers["local"] = True
    except: pass
    if os.getenv("OPENAI_API_KEY"): providers["openai"] = True
    if os.getenv("ANTHROPIC_API_KEY"): providers["anthropic"] = True
    return providers
