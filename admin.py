from fastapi import APIRouter, Body
import json, os
router = APIRouter()
CONFIG_FILE = "backend/app/config.json"

def read_conf():
    if not os.path.exists(CONFIG_FILE):
        return {"lead_output":"excel","brand":{"name":"Aqarino","primaryColor":"#0077b6"}}
    return json.load(open(CONFIG_FILE,"r",encoding="utf-8"))

def write_conf(cfg):
    json.dump(cfg, open(CONFIG_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return cfg

@router.get("/config")
async def get_config():
    return read_conf()

@router.post("/config")
async def set_config(payload: dict = Body(...)):
    cfg = read_conf()
    cfg.update(payload)
    write_conf(cfg)
    return cfg
