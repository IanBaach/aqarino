from fastapi import APIRouter, Body, HTTPException
from db import get_session, init_db
from models import Visitor, Lead, Listing, ConversationMessage
from sqlmodel import select
import json, os, csv

router = APIRouter()
init_db()

@router.post("/listings/import")
async def import_listing(payload: dict = Body(...)):
    session = get_session()
    if isinstance(payload, list):
        created = []
        for item in payload:
            l = Listing(external_id=item.get("external_id"), title=item.get("title"), city=item.get("city"), area_m2=item.get("area"), rooms=item.get("rooms"), price_tnd=item.get("price"), raw=json.dumps(item))
            session.add(l); session.commit(); session.refresh(l)
            created.append(l.id)
        return {"count": len(created), "listings": created}
    else:
        item = payload
        l = Listing(external_id=item.get("external_id"), title=item.get("title"), city=item.get("city"), area_m2=item.get("area"), rooms=item.get("rooms"), price_tnd=item.get("price"), raw=json.dumps(item))
        session.add(l); session.commit(); session.refresh(l)
        return {"id": l.id}

@router.post("/leads")
async def create_lead(payload: dict = Body(...)):
    session = get_session()
    visitor_data = payload.get("visitor", {})
    visitor = Visitor(name=visitor_data.get("name"), phone=visitor_data.get("phone"), email=visitor_data.get("email"))
    session.add(visitor); session.commit(); session.refresh(visitor)
    listing_id = None
    if payload.get("listing") and payload["listing"].get("external_id"):
        q = select(Listing).where(Listing.external_id == payload["listing"]["external_id"])
        r = session.exec(q).first()
        if r: listing_id = r.id
    lead = Lead(listing_id=listing_id, visitor_id=visitor.id, intent=payload.get("intent"), raw_message=payload.get("message"))
    session.add(lead); session.commit(); session.refresh(lead)
    cm = ConversationMessage(lead_id=lead.id, role="user", content=payload.get("message",""))
    session.add(cm); session.commit()
    qual = {"buyer_seller":"unknown","budget_min":None,"budget_max":None,"ready_to_contact":False}
    txt = (payload.get("message") or "").lower()
    if any(w in txt for w in ["buy","looking","شراء","نبحث"]): qual["buyer_seller"]="buyer"
    if any(w in txt for w in ["sell","بيع","أبيع"]): qual["buyer_seller"]="seller"
    if any(w in txt for w in ["call","contact","اتصل","تواصل"]): qual["ready_to_contact"]=True
    qmsg = ConversationMessage(lead_id=lead.id, role="system", content="qualification:"+json.dumps(qual))
    session.add(qmsg); session.commit()
    out_type = os.getenv("LEAD_OUTPUT","excel")
    if out_type == "webhook" and os.getenv("WEBHOOK_URL"):
        import httpx
        try:
            await httpx.AsyncClient().post(os.getenv("WEBHOOK_URL"), json={"lead_id": lead.id, "visitor": visitor_data, "qualification": qual}, timeout=5.0)
        except: pass
    if out_type == "email" and os.getenv("LEAD_EMAIL_TO"):
        try:
            import smtplib
            from email.message import EmailMessage
            msg = EmailMessage()
            msg["Subject"] = f"New lead #{lead.id}"
            msg["From"] = os.getenv("LEAD_EMAIL_FROM","no-reply@aqarino.local")
            msg["To"] = os.getenv("LEAD_EMAIL_TO")
            body = f"Lead #{lead.id}\nVisitor: {visitor.name} {visitor.phone} {visitor.email}\nMessage: {lead.raw_message}\nQualification: {qual}"
            msg.set_content(body)
            s = smtplib.SMTP(os.getenv("SMTP_HOST","localhost"), int(os.getenv("SMTP_PORT",25)))
            s.send_message(msg); s.quit()
        except Exception as e:
            print("email send failed", e)
    if out_type == "excel":
        fn = os.getenv("LEADS_EXPORT_FILE","leads_export.csv")
        exists = os.path.exists(fn)
        with open(fn,"a",newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["lead_id","name","phone","email","message","buyer_seller","ready_to_contact","created_at"])
            writer.writerow([lead.id, visitor.name, visitor.phone, visitor.email, lead.raw_message, qual["buyer_seller"], qual["ready_to_contact"], str(lead.created_at)])
    return {"lead_id": lead.id, "qualification": qual}

@router.get("/leads")
async def list_leads():
    session = get_session()
    q = select(Lead)
    rows = session.exec(q).all()
    out = []
    for r in rows:
        v = session.get(Visitor, r.visitor_id)
        out.append({"id": r.id, "visitor": {"name": v.name, "phone": v.phone, "email": v.email}, "intent": r.intent, "message": r.raw_message, "status": r.status, "created_at": str(r.created_at)})
    return out
