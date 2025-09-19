# Sonar Experiment API

API en FastAPI para experimento de normas descriptivas y sorteos.

## Requisitos
- Python 3.11+
- macOS/Linux/Windows

## Instalación
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints públicos
- GET `/api/public/status`
- POST `/api/public/start_session`
- POST `/api/public/roll_die?session_id=...`
- POST `/api/public/report?session_id=...&reported_value=...`
- GET `/api/public/norm?session_id=...`

Abrir Swagger en `http://localhost:8000/docs`.
