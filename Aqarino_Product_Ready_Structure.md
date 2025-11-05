Aqarino™ Product-Ready Structure
================================

Goal: package Aqarino as a white-label product for client installation on real-estate agency websites.

Structure in this package:
- backend/             (FastAPI app and static serving)
  - app/main.py        (minimal server that serves widget static files)
  - static/host/       (contains aqarino-widget-tn.umd.js)
- frontend/demo/       (demo page embedding the widget)
- Makefile, run.sh     (easy local dev commands)
- .env.example         (env templates)
- Dockerfile.backend   (optional containerization)
- docker-compose.yml   (optional local compose)

White-label notes:
- Keep Aqarino™ trademark on the widget asset unless client license says otherwise.
- To customize for a client:
  1. Update widget branding and theme colors in backend/app/static/host/aqarino-widget-tn.umd.js
  2. Optionally replace demo HTML (frontend/demo/index.html) with client pages that include the widget script tag:
     <script src="/static/host/aqarino-widget-tn.umd.js"></script>
  3. Configure client's API keys in .env (or a secure secrets manager)
  4. Provide deployment instructions or container image for the client infra.

If you want, I can also produce:
- an installer script that copies only the widget and minimal server to a client's web server,
- or an npm package hosting only the widget (for frontend teams).
