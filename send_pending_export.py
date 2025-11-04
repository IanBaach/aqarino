
#!/usr/bin/env python3
"""Send leads_export.csv as attachment via SMTP. Configure env vars:
LEADS_EXPORT_FILE (default leads_export.csv)
SMTP_HOST, SMTP_PORT, SMTP_USER (optional), SMTP_PASS (optional)
LEAD_EMAIL_TO
"""
import os, smtplib, mimetypes
from email.message import EmailMessage

fn = os.getenv("LEADS_EXPORT_FILE","leads_export.csv")
if not os.path.exists(fn):
    print("No export file found:", fn)
    raise SystemExit(1)

to_addr = os.getenv("LEAD_EMAIL_TO")
if not to_addr:
    print("Set LEAD_EMAIL_TO env to receive exports")
    raise SystemExit(1)

msg = EmailMessage()
msg["Subject"] = "Aqarino leads export"
msg["From"] = os.getenv("LEAD_EMAIL_FROM","no-reply@aqarino.local")
msg["To"] = to_addr
msg.set_content("Attached leads export file.")

ctype, _ = mimetypes.guess_type(fn)
if not ctype:
    ctype = "application/octet-stream"
maintype, subtype = ctype.split("/",1)
with open(fn,"rb") as f:
    msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(fn))

host = os.getenv("SMTP_HOST","localhost")
port = int(os.getenv("SMTP_PORT",25))
user = os.getenv("SMTP_USER")
pw = os.getenv("SMTP_PASS")

if user and pw:
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(user, pw)
else:
    s = smtplib.SMTP(host, port)
s.send_message(msg)
s.quit()
print("Sent", fn, "to", to_addr)
