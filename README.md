
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

# Task 2: Data Scraping and Collection (Extract & Load)

### 📂 Objectivies

To extract raw messages, metadata, and media (images) from selected public Telegram channels related to Ethiopian medical businesses and store them in a partitioned Data Lake for downstream processing.

---

### 👩‍💻 Telegram Scraping Overview

* **Objective**: Collect textual and visual data from public Telegram channels.
* **Channels**:

  * Chemed Telegram Channel
  * [https://t.me/lobelia4cosmetics](https://t.me/lobelia4cosmetics)
  * [https://t.me/tikvahpharma](https://t.me/tikvahpharma)
  * Additional sources from [https://et.tgstat.com/medicine](https://et.tgstat.com/medicine)

---

### 🧰 tools or modules used

* **Telethon**: Python Telegram client library for accessing the Telegram API.
* **Python**: Core scripting language for automation.
* **Logging**: Custom logging to track scraping status, error handling, and retries.

---

### 📅 Folder & Storage Strategy

All scraped raw data is stored as JSON files in a structured, partitioned directory:

```
data/
 ├── raw/
     ├── telegram_messages/
         ├── YYYY-MM-DD/
             ├── channel_name.json
```

* This format allows incremental processing and better versioning of raw data.
* JSON structure preserves original Telegram API fields: message ID, timestamp, sender, text, images, etc.

---

### 🚀 Execution Steps

1. **API Setup**

   * Created Telegram app from [https://my.telegram.org](https://my.telegram.org)
   * Secured API ID and Hash in `.env`
   * Loaded via `python-dotenv`

2. **Scraper Features**

   * Scrapes text, media, timestamps, sender IDs.
   * Supports incremental scrape (avoids duplicate messages).
   * Stores message metadata (channel name, message ID, etc.).
   * Downloads and saves image attachments into structured media folders (e.g., `data/raw/images/chemed/YYYY-MM-DD/`)
   * Logs: success/failure per channel per date.

3. **Error Handling**

   * Catches rate limit errors (FloodWait).
   * Retries on timeout and network errors.
   * Tracks scraping progress to avoid data loss or duplication.

---

### 🔎 Example JSON Output Structure

```json
{
  "channel": "chemed",
  "date": "2025-07-14",
  "message_id": 1834,
  "text": "New shipment of Amoxicillin available",
  "media_type": "image",
  "media_path": "data/raw/images/chemed/2025-07-14/amox1834.jpg"
}
```

---

### 📈 Progress Summary

| Channel Name      | Status      | Messages Collected | Media Files |
| ----------------- | ----------- | ------------------ | ----------- |
| chemed            | Completed   | 6,500+             | 250+        |
| lobelia4cosmetics | Completed   | 4,200+             | 300+        |
| tikvahpharma      | In Progress | 3,000+             | 110+        |

---

### 📅 Next Steps

* Integrate scraped data into PostgreSQL staging layer.
* Begin cleaning and transformation with dbt.
* Use YOLO for object detection on downloaded images to extract product types.

---

### 🚀 Sample Command to Run Scraper

```bash
python src/etl/scrape_telegram.py --channel chemed --days_back 5

```
 # 📊 Task-2 Data Modeling and Transformation (Transform) (dbt)

This project transforms raw Telegram messages into a clean **star schema** in PostgreSQL using **dbt**.

---

## 📂 Project Structure
```
models/
  dim_channels.sql   -- Channel info
  dim_dates.sql      -- Calendar/date
  fact_messages.sql  -- Message metrics
  schema.yml         -- Tests & docs
```

---

## 🚀 Usage
1. Install dbt (Postgres):
   ```bash
   pip install dbt-postgres
   ```
2. Configure your connection in `profiles.yml`.
3. Run models:
   ```bash
   dbt run
   ```
4. Run tests:
   ```bash
   dbt test
   ```

---

## 📐 Star Schema
- **dim_channels** → Telegram channel info  
- **dim_dates** → Calendar breakdown  
- **fact_messages** → Views, forwards, media type, text  

---

## 🔎 Example Query
```sql
-- Top 5 most viewed posts
SELECT 
    c.channel_name,
    f.message_id,
    f.views,
    f.media_type,
    f.date
FROM analytics.fact_messages f
JOIN analytics.dim_channels c
  ON f.sender_id = c.sender_id
ORDER BY f.views DESC
LIMIT 5;
```
  # Task 3 - Data Enrichment with Object Detection (YOLO)

This task uses a modern, pre-trained **YOLOv8 model** to analyze images and enrich data with detected objects. The results are stored in a PostgreSQL data warehouse for further analytics and visualization.

---

## 🚀 Workflow
1. **Setup YOLOv8 model**
   ```python
   from ultralytics import YOLO
   model = YOLO("yolov8n.pt")  # Pre-trained YOLOv8 nano model
   ```

2. **Run detection on image folders**
   ```python
   detections = run_yolo_on_folders()
   ```

3. **Store results in PostgreSQL**
   ```python
   create_table_if_not_exists()
   insert_detections(detections)
   ```

4. **Query enriched detections**
   ```sql
   SELECT * FROM analytics.fct_image_detections LIMIT 10;
   ```

5. **Visualize insights**
   - Count of detected object classes  
   - Confidence score distribution  

   ```python
   df['detected_object_class'].value_counts().plot(kind="bar")
   df['confidence_score'].hist(bins=20)
   ```

---

## 🗄️ Database Schema

Table: **`analytics.fct_image_detections`**

| Column                  | Type      | Description                       |
|--------------------------|----------|-----------------------------------|
| `id`                    | SERIAL   | Primary key                       |
| `image_path`            | TEXT     | Path of the analyzed image         |
| `detected_object_class` | TEXT     | Class label of the detected object |
| `confidence_score`      | FLOAT    | Model confidence (0–1)             |
| `detected_at`           | TIMESTAMP | Time of detection insertion        |

---

## 📊 Example Visualization

- **Detected Object Counts**
- **Confidence Distribution**

These help monitor object detection performance and provide insights into enriched datasets.

---

## 🔧 Requirements

- Python 3.9+
- PostgreSQL
- Packages: `ultralytics`, `matplotlib`, `psycopg2`, `pandas`

---

✅ With this pipeline, raw images are automatically processed, detected objects are stored in a **data warehouse**, and insights can be visualized for downstream analytics.


# 📊 Task 4 – Build an Analytical API with FastAPI  

This task sets up an **Analytical API** using **FastAPI** to query the processed medical channel data (stored in PostgreSQL + dbt models). The API provides endpoints to extract insights for business use cases.  

---

## ⚙️ Setup  

### 1. Install Dependencies  
```bash
pip install fastapi uvicorn psycopg2-binary sqlalchemy pydantic
```

### 2. Project Structure  
```
my_project/
├── main.py        # FastAPI entry point
├── database.py    # DB connection (SQLAlchemy + PostgreSQL)
├── models.py      # SQLAlchemy models (tables)
├── schemas.py     # Pydantic schemas (response validation)
└── crud.py        # Business query logic
```

---

## 🚀 Running the API  
Start the server with:  
```bash
uvicorn my_project.main:app --reload
```

Visit:  
- 👉 [Swagger Docs](http://127.0.0.1:8000/docs)  
- 👉 [Redoc UI](http://127.0.0.1:8000/redoc)  

---

## 📌 Endpoints  

### 1. **Top Products**  
Get most frequently mentioned products:  
```http
GET /api/reports/top-products?limit=10
```
Response:  
```json
[
  { "product_name": "paracetamol", "count": 120 },
  { "product_name": "amoxicillin", "count": 85 }
]
```

---

### 2. **Channel Activity**  
Get posting activity (daily counts) for a channel:  
```http
GET /api/channels/{channel_name}/activity
```
Response:  
```json
[
  { "date": "2025-08-01", "count": 45 },
  { "date": "2025-08-02", "count": 38 }
]
```

---

### 3. **Search Messages**  
Search for messages containing a keyword:  
```http
GET /api/search/messages?query=paracetamol
```
Response:  
```json
[
  {
    "id": 101,
    "channel_name": "tikva",
    "message_text": "Paracetamol 500mg available at discount",
    "posted_at": "2025-08-12T10:30:00"
  }
]
```

---

## ✅ Features  
- Built with **FastAPI** + **SQLAlchemy**  
- Modular structure for scalability  
- Automatic API documentation  
- Queries final **dbt models (data marts)** for analytics  


# Task 5 - Analytical Dashboard Integration

## 📌 Overview
In this task, we integrate the results from the **Analytical API (Task 4)** into a dashboard.  
The dashboard provides **visual insights** into products, channels, and detected objects from the data warehouse.  
It enables stakeholders to explore trends and patterns easily.

---

## ⚙️ Steps

### 1. Data Source
- Data comes from **FastAPI analytical endpoints** (Task 4).
- Example endpoints:
  - `/api/reports/top-products`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages?query=paracetamol`

### 2. Dashboard Technology
You can implement the dashboard using:
- **Streamlit** (Python-based, simple and fast)  
- or **React + Recharts** (JS-based, more customizable).  

For simplicity, we used **Streamlit**.

### 3. Implementation
Install Streamlit:
```bash
pip install streamlit requests matplotlib pandas
