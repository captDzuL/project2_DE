import pandas as pd
import requests
from io import StringIO
from sqlalchemy import create_engine

# Daftar URL file CSV
csv_files = [
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/categories.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/customers.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/employees.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/orders.csv",
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/regions.csv"
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/shippers.csv"
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/suppliers.csv"
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/order_details.csv"
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/territories.csv"
    "https://raw.githubusercontent.com/captDzuL/graphql-compose-examples/master/examples/northwind/data/csv/employee_territories.csv"
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
        df.to_sql(table_name, db, if_exists='replace', index=False)
        print(f"{table_name} telah berhasil disimpan ke dalam database.")
    else:
        print(f"Gagal mengunduh {url}")

# Mengunduh dan menyimpan setiap CSV ke dalam tabel PostgreSQL
for csv_file in csv_files:
    table_name = csv_file.split("/")[-1].replace(".csv", "")  # Menentukan nama tabel dari nama file
    download_and_save_csv(csv_file, table_name)
