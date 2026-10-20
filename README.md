# BigData Analytics & ETL Pipeline

An end-to-end data analytics and ETL pipeline project focused on relational retail sales data, dimensional modeling, and exploratory data analysis (EDA). Built with **Python**, **Pandas**, **SQL Server**, and **Jupyter Notebooks**.

---

## Architecture & Project Structure

The project is structured following standard data engineering and data science project conventions:

```plaintext
BigData/
├── data/
│   ├── csv/                   # Cleaned, consolidated relational tables (CSV)
│   │   ├── articulos.csv      # Products catalog
│   │   ├── canal.csv          # Sales distribution channels
│   │   ├── clientes.csv       # Customer demographics and origin
│   │   ├── detalle_venta.csv  # Transaction line items
│   │   ├── ubicaciones.csv    # Consolidated branch & regional locations
│   │   ├── vendedores.csv     # Sales representatives
│   │   └── ventas.csv         # Sales transaction headers
│   └── excel/                 # Raw and transformed spreadsheet sources
│       ├── Americans.xlsx     # Source multi-sheet relational workbook
│       └── Americans_limpio.xlsx # Cleaned, normalized workbook
├── notebooks/
│   └── BIG_DATA_AMERICANS.ipynb # Exploratory Data Analysis & data cleaning pipeline
├── sql/
│   └── 2.1.4_BD_Americans.sql # Database DDL and DML population script (SQL Server)
├── src/
│   ├── __init__.py
│   ├── db_connection.py       # Database connection factory (SQLAlchemy & pyodbc)
│   └── export_data.py         # Automated ETL extraction & CSV export script
├── .gitignore
├── requirements.txt           # Project dependencies
└── README.md
```

---

## Key Highlights & Pipeline Stages

### 1. Database & Schema Modeling (`sql/`)
* Contains the complete database definition (`Americans`) with star-schema relational design, encompassing sales transactions, customers, branch hierarchy (commune, province, region), and sales channels.

### 2. ETL & Extraction Pipeline (`src/`)
* **[`db_connection.py`](file:///C:/Users/seba/Documents/github/big_data/src/db_connection.py)**: Configures a reusable SQLAlchemy connection using Windows Authentication (Trusted Connection).
* **[`export_data.py`](file:///C:/Users/seba/Documents/github/big_data/src/export_data.py)**: Queries relational tables, denormalizes geographical branch data into a consolidated `ubicaciones` dimension, and exports clean datasets into `data/csv/`.

### 3. Exploratory Data Analysis & Transformation (`notebooks/`)
* **[`BIG_DATA_AMERICANS.ipynb`](file:///C:/Users/seba/Documents/github/big_data/notebooks/BIG_DATA_AMERICANS.ipynb)**:
  * Normalizes date structures and removes uniform time component noise.
  * Normalizes alphanumeric surrogate keys (`CLI0001` -> `1`) into relational integers for indexing and storage optimization.
  * Cleans string whitespace, redundant text prefixes, and validates referential integrity.
  * Exports the consolidated and cleaned model into `Americans_limpio.xlsx`.

---

## Getting Started

### Prerequisites
* Python 3.9+
* SQL Server (local instance with ODBC Driver 17, optional for running live ETL)

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:aqunavseb/BigData.git
   cd BigData
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run JupyterLab or Jupyter Notebook:
   ```bash
   jupyter lab
   ```
   Open `notebooks/BIG_DATA_AMERICANS.ipynb` to inspect the analysis and transformations.
