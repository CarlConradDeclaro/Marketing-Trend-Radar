# Marketing Trend Radar

Marketing Trend Radar is a full-stack app that pulls recent marketing-related articles, analyzes them with an LLM workflow, and displays the results in a dashboard.

## Requirements

- Node.js 18+ for the frontend
- Python 3.10+ for the backend
- `npm`
- `pip`

## Project Structure

- `backend/` - FastAPI service that fetches and analyzes trend data
- `frontend/` - Next.js dashboard UI

## Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Set the required backend values in `backend/.env`:

- `OPENAI_API_KEY`
- `LLM_MODEL`
- `FRONTEND_ORIGIN`
- `GDELT_TIMEOUT_SECONDS`

Start the API:

```bash
uvicorn app.main:app --reload
```

### 2. Frontend

Open a second terminal:

```bash
cd frontend
npm install
copy .env.example .env
```

Set the frontend API base URL in `frontend/.env`:

- `NEXT_PUBLIC_API_BASE_URL`

Start the web app:

```bash
npm run dev
```

## How To Run

1. Start the backend first.
2. Start the frontend after the API is running.
3. Open the frontend in your browser and use the dashboard to search and analyze trends.

## API Endpoints

- `GET /` - health check
- `GET /fetch-gdelt?query=AI%20marketing&max_articles=20` - returns cleaned article results
- `POST /analyze-trends` - returns the trend analysis output

## Notes

- The backend must be reachable from the frontend through `NEXT_PUBLIC_API_BASE_URL`.
- If you change environment variables, restart both servers.
