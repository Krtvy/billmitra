cat > docs/architecture.md << 'EOF'

\# BillMitra System Architecture



\## Overview



Cloud-native ML platform for retail demand forecasting.



\## Architecture Diagram

```

┌─────────────────────────────────────────────────────────────┐

│                     DATA LAYER (S3)                          │

├─────────────────────────────────────────────────────────────┤

│  raw/                processed/        models/    predictions/│

│  - daily\_sales.csv  - featured.csv    - arima/   - forecast/ │

│                                        - prophet/             │

│                                        - lstm/                │

└─────────────────────────────────────────────────────────────┘

&nbsp;                             ↓

┌─────────────────────────────────────────────────────────────┐

│                   ETL PIPELINE (Lambda)                      │

├─────────────────────────────────────────────────────────────┤

│  1. Data Ingestion    2. Cleaning     3. Feature Engineering │

│  4. Model Training    5. Prediction   6. Storage             │

└─────────────────────────────────────────────────────────────┘

&nbsp;                             ↓

┌─────────────────────────────────────────────────────────────┐

│                    ML MODELS (EC2)                           │

├─────────────────────────────────────────────────────────────┤

│  ARIMA          Prophet         LSTM                         │

│  (baseline)     (seasonal)      (deep learning)              │

└─────────────────────────────────────────────────────────────┘

&nbsp;                             ↓

┌─────────────────────────────────────────────────────────────┐

│                  API LAYER (FastAPI)                         │

├─────────────────────────────────────────────────────────────┤

│  /predict       /historical     /insights                    │

└─────────────────────────────────────────────────────────────┘

&nbsp;                             ↓

┌─────────────────────────────────────────────────────────────┐

│                 DASHBOARD (Streamlit)                        │

├─────────────────────────────────────────────────────────────┤

│  Sales Forecast │ Inventory Alert │ Pricing Suggestion      │

└─────────────────────────────────────────────────────────────┘

```



\## Components



\### 1. Data Storage (AWS S3)

\- Raw data lake

\- Processed datasets

\- Model artifacts

\- Prediction outputs



\### 2. Compute (AWS EC2)

\- Model training

\- Batch predictions

\- API hosting



\### 3. Serverless (AWS Lambda)

\- Automated ETL

\- Scheduled retraining

\- Event-driven processing



\### 4. Database (AWS RDS PostgreSQL)

\- User data

\- Product catalog

\- Historical predictions



\### 5. Monitoring (CloudWatch)

\- Cost tracking

\- API metrics

\- Model performance



\## Security



\- IAM roles with least privilege

\- No hardcoded credentials

\- VPC for database

\- Encrypted S3 buckets

\- API authentication



\## Cost Optimization



\- Free tier usage maximized

\- Spot instances for training

\- S3 lifecycle policies

\- Lambda for intermittent tasks

\- RDS in free tier (t3.micro)



\*\*Current monthly cost\*\*: $0 (within free tier)

EOF

