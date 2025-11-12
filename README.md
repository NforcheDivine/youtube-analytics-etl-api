# 🎬 YouTube Analytics ETL Pipeline

![API Documentation](images/api-docs.png)
![Pipeline Running in Terminal](images/terminal-run.png)

## 🚀 Overview
The **YouTube Analytics ETL Pipeline** automates the extraction of raw YouTube data, transforms it into structured insights, and loads it into a database accessible via a **FastAPI** REST interface.  
This project demonstrates professional ETL design, API development, and data workflow automation.

---

## 💼 Business Value
- Converts raw YouTube data into **actionable business insights**  
- Provides a **REST API** for dashboards, analytics tools, and apps  
- Demonstrates **end-to-end data engineering workflow** — extraction, transformation, and loading  
- Easy to deploy and scale for production data workflows  

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FFCA28?style=for-the-badge&logo=python&logoColor=black)

---

## 📂 Project Structure
```
youtube-pipeline/
├── data/                   # raw YouTube CSVs or API data
├── scripts/                # ETL scripts (extract, transform, load)
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── database/
│   └── schema.sql          # SQLite schema
├── api.py                  # FastAPI endpoints
├── run_api.py              # starts the REST API
├── main.py                 # orchestrates the ETL pipeline
├── requirements.txt        # dependencies
├── .env                    # environment variables (ignored by git)
├── .gitignore              # git ignore rules
└── README.md               # documentation
```

---

## ⚙️ How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/NforcheDivine/youtube-analytics-etl-api.git
cd youtube-analytics-etl-api
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API
```bash
python run_api.py
```

Open your browser and navigate to:  
👉 **http://localhost:8000/docs**

---

## 📊 Example Endpoints

- **`/extract`** – pulls YouTube data from source  
- **`/transform`** – cleans and prepares the data  
- **`/load`** – inserts processed data into the SQLite database  
- **`/health`** – simple API health check  

---

## 📘 Future Improvements
- Add Docker Compose support for database + API containers  
- Integrate with Google YouTube Data API for real-time analytics  
- Schedule ETL with Airflow or Prefect  

---

## 👨‍💻 Author
**Nforche Divine Ako**  
📧 [nforchedivine@gmail.com](mailto:nforchedivine@gmail.com)  
💼 [LinkedIn](https://linkedin.com/in/nforche-divine-ako-7a821889)

---

⭐ *If you like this project, consider starring it to support future improvements!*
