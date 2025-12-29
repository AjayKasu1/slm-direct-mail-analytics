# Share Local Media - Direct Mail Analytics

## Project Overview
This portfolio project simulates and analyzes direct mail marketing campaign data. It includes data enrichment, exploratory analysis via Jupyter Notebook, and an interactive Streamlit dashboard.

## Folder Structure
- `Dataset/`: Contains the raw and enriched CSV files.
- `data_prep.py`: Script to enrich raw data with simulated metrics (Revenue, CPA, ROAS).
- `analysis.ipynb`: Jupyter Notebook for deep dive analysis and categorization.
- `app.py`: Streamlit dashboard for interactive visualization.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run Data Preparation:
   ```bash
   python data_prep.py
   ```
   This generates `Dataset/direct_mail_campaigns_enriched.csv`.

3. Run the Dashboard:
   ```bash
   streamlit run app.py
   ```

## Features
- **Data Enrichment**: Calculates synthetic performance metrics.
- **Market Tiers**: Segments locations into Top, Middle, and Lower tiers based on CPA efficiency.
- **Interactive Dashboard**:
    - Filter by Channel and Market Tier.
    - View KPI cards (Revenue, CPA, ROAS).
    - Analyze charts for Channel performance and Tier efficiency.
    - "Gravity View": A scatter plot visualizing efficiency vs scale.
