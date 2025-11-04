
# CURL Examples for Aqarino v2

Assuming backend at http://localhost:8000

## Detect providers
curl http://localhost:8000/api/detect

## Import listing
curl -X POST http://localhost:8000/api/listings/import -H "Content-Type: application/json" -d '{"external_id":"L123","title":"2-bed Apt","city":"Sousse","area":95,"rooms":2,"price":120000}'

## Create a lead (widget would do this)
curl -X POST http://localhost:8000/api/leads -H "Content-Type: application/json" -d '{"visitor":{"name":"Ali","phone":"+21612345678"}, "listing":{"external_id":"L123"}, "message":"Is this available? I want to buy."}'

## List leads
curl http://localhost:8000/api/leads
