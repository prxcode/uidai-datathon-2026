   # UIDAI Datathon 2026 - Project NeevDrishti

**Aadhaar Lifecycle Intelligence (ALI)** - A comprehensive data analytics solution for identifying operational inefficiencies and service gaps in the Aadhaar ecosystem.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## Overview

Project ALI transforms raw Aadhaar operational data into actionable intelligence for UIDAI administrators. By analyzing demographic demand, biometric updates, and enrolment patterns across India's 1.4 billion population, we identify:

- **Coverage Gaps**: Districts with low enrolment relative to population
- **Service Strain**: Zones where biometric update demand exceeds supply
- **Operational Anomalies**: Irregular patterns indicating system issues
- **Priority Zones**: Data-driven recommendations for mobile camp deployment

---

## Project Structure

```
uidai-datathon-2026/
├── data/
│   ├── raw/                      # Immutable: Aadhaar datasets (CSV files)
│   │   ├── biometric/            # Biometric update records
│   │   ├── demographic/          # Population demographic data
│   │   └── enrolment/            # New Aadhaar generation records
│   └── processed/                # SSI scores and cleaned pincode aggregates
├── notebooks/
│   ├── 01_EDA.ipynb             # Exploratory Data Analysis
│   └── 02_SSI_Model.ipynb       # Service Strain Index model
├── src/                          # Production-ready Python modules
│   ├── __init__.py              # Package initialization
│   ├── data_loader.py           # Big Data ETL logic (glob + pandas)
│   └── analytics.py             # Mathematical SSI calculation
├── reports/
│   ├── figures/                 # Exported visualizations
│   └── Final_Report.pdf         # Formal submission report
├── dashboard.py                  # Streamlit interactive dashboard
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for cloning)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/prxcode/uidai-datathon-2026.git
   cd uidai-datathon-2026
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running Jupyter Notebooks

Launch Jupyter and explore the analysis:

```bash
jupyter notebook
```

Navigate to `notebooks/` and open:
- `01_EDA.ipynb` - Complete exploratory data analysis with visualizations
- `02_SSI_Model.ipynb` - Service Strain Index model demonstration

### Running the Interactive Dashboard

Launch the Streamlit dashboard for interactive data exploration:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501` with three tabs:
- **Biometric**: Biometric update analysis with 2D charts and 3D state maps
- **Demographic**: Population distribution analysis
- **Enrolment**: New registration trends

---

## Data Sources

This project uses three primary datasets from UIDAI APIs:

### 1. Demographic Dataset
- **Content**: Daily population counts by pincode, district, and state
- **Segmentation**: Age groups (0-5, 5-18, 18+)
- **Purpose**: Establishes baseline demand for services

### 2. Enrolment Dataset
- **Content**: Daily counts of new Aadhaar registrations
- **Purpose**: Measures service inflow and coverage expansion

### 3. Biometric Update Dataset
- **Content**: Counts of biometric updates (MBU/CBU)
- **Purpose**: Tracks lifecycle maintenance and update compliance

---

## Key Findings

Our analysis revealed:

1. **Demographic Concentration**: 20% of districts account for 80% of enrolment activity
2. **Service Gap**: Weak correlation (0.6) between demographic demand and biometric supply
3. **Priority Districts**: Identified top 10 districts with highest service backlog
4. **SSI Hotspots**: High Service Strain Index zones requiring immediate intervention

---

## Service Strain Index (SSI)

The core innovation of Project ALI is the **Service Strain Index**:

$$SSI = \frac{\text{Demographic Demand}}{\text{Biometric Supply} + 1}$$

**Interpretation:**
- SSI < 1.0: Well-served (supply exceeds demand)
- SSI = 1.0: Equilibrium
- SSI > 1.5: High strain (under-served, priority intervention needed)

See `notebooks/02_SSI_Model.ipynb` for detailed methodology.

---

## Technical Stack

- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Dashboard**: Streamlit, pydeck
- **Analysis**: Jupyter notebooks
- **Version Control**: Git

---

## Methodology

### 1. Data Ingestion & Preprocessing
- Recursive CSV loading from fragmented logs
- State name standardization (e.g., "Orissa" → "Odisha")
- Garbage value filtering

### 2. Data Cleaning
- Mapping inconsistent state names to LGD standards
- Removing null values and test entries
- Validation against official state whitelist

### 3. Aggregation Strategy
- District-level: Operational resource allocation
- State-level: High-level policy dashboarding
- Time-series: Seasonal trend identification

### 4. Metric Derivation
- **Coverage Ratio**: Enrolment / Population
- **Update Compliance**: Biometric Updates / Demographic Population
- **Service Strain Index**: Demand / Supply ratio

---

## Recommendations

Based on our analysis, we recommend:

1. **Deploy Mobile Units**: Target high-SSI districts identified in analysis
2. **Investigate Systemic Issues**: Analyze under-performing regions for infrastructure gaps
3. **Predictive Scheduling**: Use demographic trends to pre-position resources
4. **Infrastructure Enhancement**: Permanent upgrades in consistently strained zones

---


## License

This project is licensed under the MIT License - see the LICENSE file for details.



