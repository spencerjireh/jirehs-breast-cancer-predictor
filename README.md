# CytoLens

CytoLens is a breast cancer predictor for cancer malignancy in breast tissue samples meant to be used in conjunction with measurements from a cytology lab. Uses a Logistic Regression model with an interactive radar chart visualization.

Built with **FastAPI** (backend) + **Svelte** (frontend), served from a single Docker container.

Thank you to [Alejandro AO](https://github.com/alejandro-ao).

## Development

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server runs on port 5173 and proxies `/api` requests to `localhost:8000`.

### Retrain Model

```bash
cd backend
source .venv/bin/activate
python3 train.py
```

## Docker

```bash
docker build -t cytolens .
docker run -p 8000:8000 cytolens
```

Open `http://localhost:8000` to use the app.
