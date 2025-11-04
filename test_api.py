
import requests
import os
BASE = os.getenv("AQA_BASE","http://localhost:8000")
def test_detect():
    r = requests.get(f"{BASE}/api/detect")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)

def test_create_listing_and_lead():
    # create listing
    listing = {'external_id':'TST1','title':'Test Apt','city':'TestCity','area':50,'rooms':2,'price':50000}
    r = requests.post(f"{BASE}/api/listings/import", json=listing)
    assert r.status_code == 200
    data = r.json()
    assert 'id' in data or 'listings' in data
    # create lead
    lead = {'visitor':{'name':'Test','phone':'0123'}, 'listing':{'external_id':'TST1'}, 'message':'I want to buy'}
    r2 = requests.post(f"{BASE}/api/leads", json=lead)
    assert r2.status_code == 200
    j = r2.json()
    assert 'lead_id' in j
