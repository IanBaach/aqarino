
#!/usr/bin/env bash
# Run pytest against local running backend (must be on http://localhost:8000)
pytest -q --disable-warnings -o log_cli=true
