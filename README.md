# 🎬 YouTube Analytics ETL Pipeline (with REST API)

Production-style project that **extracts, transforms, and loads** YouTube data, stores it in SQLite, and exposes results through a **FastAPI** REST API.

## 💼 Business Value
- Turn raw YouTube data into **actionable insights** (videos, channels, trends)
- **API** enables dashboards and app integrations
- Clear, professional structure that mirrors real projects

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-003B57)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC)

## 📂 Project Structure
youtube-pipeline/
├── data/ # raw csvs (channels.csv, videos.csv)
├── database/
│ └── schema.sql # DB schema
├── scripts/ # ETL steps
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── api.py # FastAPI app (endpoints)
├── run_api.py # uvicorn runner
├── main.py # optional ETL orchestration
├── requirements.txt
├── .env # env vars (not committed)
└── README.md


## 🚀 Quickstart
```bash
pip install -r requirements.txt
python run_api.py

Open:

📘 API Docs: http://localhost:8000/docs

🌐 Health: http://localhost:8000/health

🧠 Example Endpoints
Method	Route	Description
GET	/videos	Processed video analytics
GET	/channels	Aggregated channel metrics
POST	/refresh	Trigger ETL refresh (extract→load)


