# West-Bengal-Election-Analytics-Suite-2009-2024-
West Bengal Election Analytics Suite (2009–2024) A full-stack analytics solution predicting 2026 election outcomes. Features a custom Python/Pandas ETL pipeline for data explosion and an advanced Tableau dashboard with dynamic "Swing Calculation" and parameter-based granularity control.
# West Bengal Election Analytics Suite (2009–2024) 🗳️

![Tableau](https://img.shields.io/badge/Tableau-2024.2-E97627?style=for-the-badge&logo=Tableau&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?style=for-the-badge&logo=pandas&logoColor=white)

### 📊 [View Live Dashboard on Tableau Public](https://public.tableau.com/shared/XBH7D9NHD?:display_count=n&:origin=viz_share_link)

## 📖 Project Overview
This project is an end-to-end analytics solution designed to analyze historical voting trends in West Bengal (2009–2024) and simulate future scenarios for the 2026 Assembly Elections.

Unlike standard visualizations that rely on pre-aggregated data, this project uses a **custom Python ETL pipeline** to reverse-engineer "True Vote Share" from raw election records, enabling granular analysis of third-party vote fragmentation.

## 🛠️ Technical Architecture

### 1. Data Engineering (Python & Pandas)
* **Problem:** Raw Election Commission of India (ECI) data is "Wide Format" (Winner/Runner columns), which hides the true vote share of third-party candidates and makes total vote share calculations impossible.
* **Solution:** Built a Python script (`ETL_Data_Transformation.py`) to:
    * **Explode** the dataset from Wide to Long format.
    * **Synthesize** a "Others" category row by calculating: `Total Votes - (Winner + Runner)`.
    * **Clean** inconsistent constituency names across 15 years of data.

### 2. Advanced Visualization (Tableau)
* **Dynamic Swing Calculator:** Implemented complex **Level of Detail (LOD)** expressions to allow users to simulate a **±10% Vote Swing** for major parties and instantly see the impact on Seat Projections.
* **Granularity Conflict Resolution:** Solved data blending errors (Logical Table vs. Aggregated Data) by implementing a **Global Parameter System** that drives filtering across disparate data sources without breaking the blend.

## 📂 File Structure

| File Name | Description |
| :--- | :--- |
| `ETL_Data_Transformation.py` | **The Engine.** Python script that transforms raw election data into analysis-ready CSVs. |
| `Final_Master_Dataset.csv` | Cleaned historical data used for the Map and Seat Count. |
| `All_Candidates_Master.csv` | Transformed "Long Data" used for the Vote Share Pie Charts. |
| `West_Bengal_Election_Dashboard.twbx` | The packaged Tableau workbook (Logic & Visualization). |

## 🚀 How to Run the ETL Script

If you want to reproduce the data engineering steps:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/West-Bengal-Election-Analytics.git](https://github.com/YOUR_USERNAME/West-Bengal-Election-Analytics.git)
    ```
2.  **Install Dependencies**
    ```bash
    pip install pandas numpy
    ```
3.  **Run the Pipeline**
    ```bash
    python ETL_Data_Transformation.py
    ```


## 👤 Author
**Shoubhik Saha**

---
*Note: This project is for educational and analytical purposes. Data is sourced from the Election Commission of India (ECI).*
