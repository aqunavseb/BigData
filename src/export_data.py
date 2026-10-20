"""ETL export module: Extracts relational tables from SQL Server, consolidates

dimensional data (locations), and exports clean datasets into CSV format.
"""

from db_connection import get_connection
import pandas as pd
import os
import sys

def get_data(output_dir=None):
    """Extract relational tables, consolidate store locations, and export to CSV files."""
    if output_dir is None:
        # Default to data/csv/ relative to project root, or current directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
        csv_dir = os.path.join(project_root, "data", "csv")
        output_dir = csv_dir if os.path.isdir(csv_dir) else "."

    os.makedirs(output_dir, exist_ok=True)

    cnx = get_connection()
    if cnx is None:
        print("Aborting: No active database connection.", file=sys.stderr)
        return

    try:
        # 1. CLIENTS (CLIENTES)
        clientes_query = "SELECT NRO, ID_CLIENTE, EDAD, RESIDENCIA, ORIGEN FROM CLIENTES"
        df_clientes = pd.read_sql(clientes_query, cnx)
        df_clientes["RESIDENCIA"] = df_clientes["RESIDENCIA"].str.strip()
        df_clientes["ORIGEN"] = df_clientes["ORIGEN"].str.strip()

        print("\nLoaded DataFrame: CLIENTES")
        print(df_clientes.head(10))

        # 2. LOCATIONS (Consolidate Store, Commune, Province, Region into UBICACIONES)
        df_comuna = pd.read_sql("SELECT * FROM COMUNA", cnx)
        df_provincia = pd.read_sql("SELECT * FROM PROVINCIA", cnx)
        df_region = pd.read_sql("SELECT * FROM REGION", cnx)
        df_sucursal = pd.read_sql("SELECT * FROM SUCURSAL", cnx)

        # Merge relational location tables
        df_locations = df_sucursal.merge(df_comuna, on="COMUNA_ID", how="left") \
                                  .merge(df_provincia, on="PROVINCIA_ID", how="left") \
                                  .merge(df_region, on="REGION_ID", how="left")

        print("\nMerged DataFrame: UBICACIONES (with foreign keys)")
        print(df_locations.head(10))

        # Select relevant columns and standardize identifier
        df_final_locations = df_locations[
            ["SUCURSAL_ID", "NOMBRE_SUCURSAL", "CIUDAD_COMUNA", "PROVINCIA", "REGION"]
        ].rename(columns={"SUCURSAL_ID": "UBICACION_ID"})

        print("\nFinal DataFrame: UBICACIONES (cleaned and standardized)")
        print(df_final_locations.head(10))

        # 3. PRODUCTS (ARTICULOS)
        df_articulos = pd.read_sql("SELECT * FROM ARTICULOS", cnx)

        # 4. SALES CHANNELS (CANAL)
        df_canal = pd.read_sql("SELECT * FROM CANAL", cnx)

        # 5. SALES DETAILS (DETALLE_VENTA)
        df_detalle_venta = pd.read_sql("SELECT * FROM DETALLE_VENTA", cnx)

        # 6. SALES REPS (VENDEDORES)
        df_vendedores = pd.read_sql("SELECT * FROM VENDEDORES", cnx)

        # 7. SALES TRANSACTIONS (VENTAS)
        df_ventas = pd.read_sql("SELECT * FROM VENTAS", cnx)

        # 8. Export all tables to CSV
        tables_to_export = {
            "ubicaciones.csv": df_final_locations,
            "clientes.csv": df_clientes,
            "articulos.csv": df_articulos,
            "canal.csv": df_canal,
            "detalle_venta.csv": df_detalle_venta,
            "vendedores.csv": df_vendedores,
            "ventas.csv": df_ventas,
        }

        for filename, df in tables_to_export.items():
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False, sep=";", encoding="utf-8-sig")
            print(f"Exported: {filepath}")

        print("\nAll datasets were successfully exported to CSV.")

    except Exception as e:
        print(f"An error occurred during data export:\n{e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    get_data()
