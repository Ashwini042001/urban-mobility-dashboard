# NYC Urban Mobility Dashboard

🚕 **NYC Yellow Taxi Trips Dashboard** is an interactive data analytics application built with Streamlit. It provides rich visualizations and insights into New York City taxi trip data using a large dataset of trip records, fare details, pickup/dropoff zones, and trip timings.

---

## Project Overview

This project analyzes NYC taxi trip data to explore trip patterns, revenue, tips, speeds, and other metrics. It offers powerful filters and visualizations to help understand urban mobility and taxi business dynamics in NYC.

Features include:
- Daily and hourly trip volume trends
- Revenue and fare analysis
- Trip speed and duration distributions
- Pickup/dropoff zone insights
- Heatmaps and scatter plots for detailed exploration
- Data export functionality for offline analysis

---

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly
- SQLite3

You can install the required Python packages using:

```bash
pip install streamlit pandas numpy plotly
Dataset and Data Files
Large Dataset Notice
The raw NYC taxi trip data files and the SQLite database are not included in this repository due to their large size (exceeding GitHub limits).

Downloading Data
You can download the raw trip data from the official NYC Taxi & Limousine Commission website:

NYC TLC Trip Record Data

The project expects the following files:

File	Description	Expected Path in Project
yellow-tripdata-YYYY-MM.csv	Raw taxi trip CSV data	data/raw/yellow-tripdata-YYYY-MM.csv
taxi_zone_lookup.csv	Lookup table for taxi zones	data/lookup/taxi_zone_lookup.csv
nyc_mobility.db	SQLite database with preprocessed data	db/nyc_mobility.db

Preparing Data
Place the downloaded CSV files under data/raw/.

Ensure the lookup CSV file (taxi_zone_lookup.csv) is present in data/lookup/.

You may use the included scripts in scripts/ folder to preprocess CSVs into the SQLite database if you want to rebuild it locally.

How to Run
From the project root directory, run the Streamlit app with:

bash
Copy
Edit
streamlit run scripts/app.py
This will launch the interactive dashboard in your default web browser.

Folder Structure
graphql
Copy
Edit
urban-mobility-dashboard/
├── data/
│   ├── raw/                   # Raw CSV data files (not in repo)
│   └── lookup/                # Lookup tables (included)
├── db/                       # SQLite database (not in repo)
├── scripts/                  # Python scripts including the Streamlit app
│   └── app.py
│   └── create_db.py
│   └── ...
├── README.md                 # Project documentation
Notes on Large Files
GitHub limits file sizes to 100 MB. Therefore:

Large files like trip data CSVs and the SQLite database are excluded from the repo.

Consider using Git Large File Storage (Git LFS) if you want to version large data files.

Alternatively, store large files on cloud storage and download them manually.

Contributing
Contributions and suggestions are welcome! Feel free to open issues or submit pull requests.

License
This project is licensed under the MIT License.

Contact
Ashwini Deshpande
GitHub: https://github.com/Ashwini042001
Email: ashwinideshpande2001@gmail.com


## Live Demo

Check out the live dashboard here:  
[NYC Taxi Dashboard - Streamlit App] https://urban-mobility-dashboard-imcixhhchh5smutncu7g5c.streamlit.app/
