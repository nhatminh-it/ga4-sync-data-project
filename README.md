# GA4 Data Sync Project with Docker

## Overview
This project syncs data from Google Analytics 4 (GA4) to a MySQL database using AWS Chalice, with Docker integration for easy deployment.

## Setup Instructions

### 1. Clone the project
```bash
git clone https://github.com/nhatminh-it/ga4-sync-data-project.git
cd ga4-sync-data-project
```
### 2. Build and run Docker containers
```bash
docker-compose up --build
```
### 3. Access Chalice App
The app will be available at `http://localhost:8000`.
### 4. Create database and table in MySQL
Connect to the `mysql-db` container and run `create_db.sql`:
```bash
docker exec -it mysql-db mysql -u your-username -p ga4_data < create_db.sql
```
### 5. Configure GA4 credentials
Ensure the credentials file is in the `path/to/your/credentials.json` and referenced correctly in `app.py`.

## Running the Project
- The daily and monthly jobs run automatically as scheduled.
- Use the /sync-data endpoint to trigger custom syncs.

- Example of Custom Data Sync Request:
```bash
curl -X POST http://localhost:8000/sync-data -d '{"start_date": "2024-10-01", "end_date": "2024-10-31"}'
```

## Notes
- Ensure the `docker-compose.yml` environment variables are set properly.
- Make sure the GA4 credentials are configured securely.