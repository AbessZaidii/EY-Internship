EY Internship Project: SDG Anomaly Dashboard & FastAPI Backend

This repository contains the full implementation of a dual-component project developed during a 3-month internship at EY. It focuses on visualizing and analyzing Sustainable Development Goal (SDG) indicators, with particular emphasis on SDG Goal 3: Good Health and Well-being.

⸻

🔧 Project Structure

EY-Internship/
├── streamlit_app/          # Streamlit frontend dashboard
├── fastapi_backend/        # FastAPI backend service
├── UNSDG/                  # Supporting datasets and files
├── sdgMain.jpeg            # Dashboard image asset
└── README.md               # Project overview (you are here)


⸻

SDG Dashboard (Streamlit Frontend)

The streamlit_app/ folder contains a data visualization dashboard built using Streamlit. It allows users to:

Features
	•	Upload datasets (CSV format) for selected countries
	•	Visualize health-related SDG Goal 3 KPIs
	•	Compare countries side-by-side
	•	Detect and highlight anomalies in data
	•	Display contextual messages, dependencies, and health trends

Running the App

cd streamlit_app
pip install -r requirements.txt
streamlit run main.py


⸻

FastAPI Backend

The fastapi_backend/ folder provides backend services to support the dashboard. Built using FastAPI, it enables modular backend operations for future integrations.

Capabilities
•	File parsing and validation
•	Custom API endpoints for KPI analysis
•	Anomaly detection logic

Running the Backend

cd fastapi_backend
pip install -r requirements.txt
uvicorn main:app --reload

Swagger Docs:

Once running, access API docs at:
http://localhost:8000/docs

⸻

Dependencies

Make sure to install the necessary packages for both components:

pip install -r streamlit_app/requirements.txt
pip install -r fastapi_backend/requirements.txt

You may use virtualenv to isolate the environments.

⸻

📊 Data Source

The dashboard works with datasets exported from:
	•	UN SDG Data Portal
	•	Internally processed or cleaned country-wise KPI datasets

⸻

📷 Image Asset
	•	sdgMain.jpeg: Used for branding or layout within the dashboard

⸻

Acknowledgement

This project was developed under the mentorship of Vaishali Ma’am during a 3-month internship at EY.

Special thanks to the EY Analytics and Development team for their support.

⸻

Contact

Abess Zaidii
abesszaidii@gmail.com
+91 9900061897

