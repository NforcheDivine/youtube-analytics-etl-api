# 🎬 YouTube Analytics ETL Pipeline

A complete **YouTube Analytics ETL pipeline** built with **Python** and **FastAPI**.  
It extracts, transforms, and loads YouTube data, then serves it through a REST API.

## 🚀 Overview
- Extracts data from CSV files (`videos.csv`, `channels.csv`)
- Transforms and loads it into an SQLite database
- Exposes analytics results through FastAPI endpoints

## ⚙️ Run the Project
```bash
pip install -r requirements.txt
python run_api.py
