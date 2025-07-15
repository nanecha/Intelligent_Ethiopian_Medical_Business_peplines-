
# Intelligent Medical Product Analysis Data Platform

This repository contains the code and infrastructure for building an end-to-end ELT data platform to analyze Ethiopian medical product data scraped from public Telegram channels. It follows modern data engineering practices and supports robust, reproducible pipelines.

---

## 🌎 Project Overview

The project aims to answer key business questions such as:

* What are the top 10 most frequently mentioned medical products?
* How does price or availability vary across channels?
* Which channels have the most visual (image-based) content?
* What are daily and weekly trends in posting volume?

The platform uses:

* **Telegram API + Telethon** for scraping messages & images
* **PostgreSQL** for the data warehouse
* **dbt** for in-warehouse transformation (raw → staging → marts)
* **YOLO** for object detection
* **FastAPI** to expose an analytical API

---

## 📁 Folder Structure

```bash
IntelligentMedicalPipeline/
├── data/                        # Data Lake & processed data
│   ├── raw/                    # Raw scraped JSON from Telegram
│   ├── staging/                # Intermediate transformation
│   └── warehouse/              # dbt or cleaned CSVs
├── notebooks/                  # EDA & prototyping
├── src/                        # Source code
│   ├── scraping/              # Telegram scraping logic
│   ├── ingestion/             # Load to PostgreSQL
│   ├── detection/             # YOLO integration
│   ├── dbt_project/           # dbt transformations
│   └── api/                   # FastAPI backend
├── docker/                     # Docker setup
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Compose file for DB + app
├── .env                        # Secrets (not committed)
└── .gitignore                 # Ignore sensitive/irrelevant files
```

---

## 🏑 Project Setup (Task 0)

### 1. Clone the repository

```bash
git clone https://github.com/<yourusername>/IntelligentMedicalPipeline.git
cd IntelligentMedicalPipeline
```

### 2. Create `.env` file

Create a `.env` file with the following values:

```env
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_PHONE_NUMBER=+251912345678
DB_HOST=db
DB_PORT=5432
DB_NAME=medicaldb
DB_USER=postgres
DB_PASSWORD=postgres
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Use Docker to run everything

```bash
cd docker
docker-compose up --build
```

This launches:

* A Python app container
* A PostgreSQL database container

---

## 💡 Key Technologies

* Python 3.11
* Telethon (Telegram scraping)
* PostgreSQL (data warehouse)
* dbt-core & dbt-postgres (transformations)
* YOLOv5 (object detection)
* FastAPI (analytical API)
* Docker + docker-compose (environment reproducibility)

---

## 🚀 Quick Start

To load secrets:

```python
from src.config import TELEGRAM_API_ID, DB_HOST
```

To run scraping:

```bash
python src/scraping/scrape_telegram.py
```

To load into DB:

```bash
python src/ingestion/load_to_db.py
```

To build warehouse:

```bash
cd src/dbt_project
dbt run
```

---



---
