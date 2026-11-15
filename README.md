## 🏎️ F1 Analytics Dashboard
An interactive Formula 1 statistics dashboard built with Python, PostgreSQL, FastAPI, and streamlit. Ingests race data from the Fastf1 library into a SQL database and serves it through a small FastAPI backend to a multi-page Streamlit frontend.

Built as a personal portfolio project to demonstrate end-to-end data engineering and analytics skills: data ingestion, relational modelling, tested query layers, and dashboard design.

## ✨ Features

- **Home** — live championship standings (drivers & constructors), leader gaps, races remaining
- **Driver Head-to-Head** — compare two teammates on points, wins, poles, DNFs, average grid/finish
- **Driver History** — career statistics for any driver in the database
- **Lap Analysis** — lap-time exploration by race and driver
- **Season Comparison** — driver and constructor performance across a season
- **Tire & Pit Strategy** — stint and pit stop analysis

<!-- Add 2-3 screenshots to docs/images/ and uncomment:
![Home page](docs/images/home.png)
![Head-to-head](docs/images/h2h.png)
-->

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Data source | FastF1 (Python F1 timing/telemetry library) |
| Database | PostgreSQL, SQLAlchemy ORM, Alembic migrations |
| Backend | FastAPI (REST API over the query layer) |
| Frontend | Streamlit (multi-page app) |
| Testing | pytest, pytest fixtures with transaction rollback |

## 🏗️ Architecture

```javascript
FastF1 API ──► ingestion scripts ──► PostgreSQL ──► FastAPI ──► Streamlit
 (raw data)   (historical_ingest,   (star-ish schema:      (repositories  (dashboard
               backfill_season)      dim_drivers,            = tested       pages)
                                     dim_races,              query layer)
                                     dim_Constructor,
                                     fact_session_result,
                                     fact_lap_summary)
```
- **Ingestion** scripts fetch raw session data once and load it into the warehouse-style schema, so dashboard reads are fast and don't hammer the upstream API
- **Repositories** (`app/repositories.py`) are the only code that touches the database from the API — fully covered by pytest against a real test database
- **Streamlit pages** call the FastAPI layer, never the database directly

## 📁 Project Structure

```javascript
.
├── app/                  # FastAPI application
│   ├── main.py           # API entry point
│   ├── database.py       # Engine, session factory, Base
│   ├── models.py         # SQLAlchemy models (dim/fact tables)
│   ├── schemas.py        # Pydantic response models
│   ├── repositories.py   # Query layer (the tested part)
│   ├── data_loader.py    # FastF1 ingestion helpers
│   └── ingest_*.py       # One-off / backfill ingestion scripts
├── routers/              # API route modules
├── frontend/             # Streamlit app
│   ├── Home.py
│   └── pages/            # Driver_H2H, Driver_History, Lap_Analysis, ...
├── scripts/              # Utility / maintenance scripts
├── alembic/              # Database migrations
├── tests/                # pytest suite (repository tests, real test DB)
├── .env                  # DATABASE_URL, TEST_DATABASE_URL (never committed)
├── requirements.txt
└── requirements-dev.txt
```

## 🚀 Getting Started

```bash
# 1. Clone and set up environment
git clone https://github.com/AndrewHampton-dev/f1-dashboard.git
cd f1-dashboard-main
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environmen
cp .env.example .env        # or create .env manually
# .env needs:
#   DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/f1_db
#   TEST_DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/f1_test

# 3. Create schema
alembic upgrade head

# 4. Load data (one-off; adjust season as needed)
python -m app.historical_ingest --season 2025

# 5. Run the API
uvicorn app.main:app --reload    # docs at http://localhost:8000/docs

# 6. Run the dashboard (second terminal)
streamlit run frontend/Home.py
```

## 🧪 Testing

```bash
pytest tests/ -v
```

Repository tests run against a real PostgreSQL test database (`TEST_DATABASE_URL`), with each test wrapped in a transaction rollback for isolation. The suite covers driver creation/constraints, race results, and championship standings arithmetic.

## 🔭 Roadmap

- [x] Multi-page dashboard with standings, H2H, and lap analysis
- [x] Database-backed query layer with pytest coverage
- [ ] Migrate Streamlit pages from direct FastF1 calls to the FastAPI layer
- [ ] Deploy (PostgreSQL + API + dashboard)
- [ ] Tire degradation / undercut-overcut strategy analysis writeup

## 📊 A sample insight

> *(Replace with one real finding from your data once written — e.g., "Across the 2025 season, the undercut gained an average of X seconds at street circuits but lost Y at high-deg tracks like Suzuka.")*

📜 License

MIT (see LICENSE)
