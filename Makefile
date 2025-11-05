.PHONY: venv install run
venv:
	python -m venv .venv
install: venv
	. .venv/bin/activate && pip install -r backend/requirements.txt
run:
	. .venv/bin/activate && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
