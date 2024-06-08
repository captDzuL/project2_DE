from fastapi import FastAPI, HTTPException
import pandas as pd
import requests
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

# Daftar URL file CSV
csv_files = [
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/categories.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/customers.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/employees.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/orders.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/products.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/employee_territories.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/order_details.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/regions.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/shippers.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/suppliers.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/territories.csv"
    # Tambahkan URL lainnya jika diperlukan
]

# Koneksi ke database PostgreSQL
db_string = "postgresql://postgres:admin@localhost/db_project2"
db = create_engine(db_string)

# Fungsi untuk mengunduh dan menyimpan CSV ke dalam PostgreSQL
def download_and_save_csv(url, table_name):
    response = requests.get(url)
    if response.status_code == 200:
        data = StringIO(response.text)
        df = pd.read_csv(data)
        try:
            df.to_sql(table_name, db, if_exists='replace', index=False)
            return f"{table_name} telah berhasil disimpan ke dalam database."
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail=f"Gagal mengunduh {url}")

# Endpoint untuk memulai proses pengunduhan dan penyimpanan CSV
@app.get("/download_and_save_all_csv/")
async def download_and_save_all_csv():
    results = []
    for csv_file in csv_files:
        table_name = csv_file.split("/")[-1].replace(".csv", "")  # Menentukan nama tabel dari nama file
        result = download_and_save_csv(csv_file, table_name)
        results.append(result)
    return {"message": "Proses selesai", "results": results}
