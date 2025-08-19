
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
