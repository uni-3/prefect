#from prefect_duckdb.database import DuckDBConnector
from prefect_duckdb import DuckDBConnector
from prefect.variables import Variable
from prefect.blocks.system import Secret

import duckdb
import dotenv

import os
# .envファイルの内容を環境変数として読み込む
dotenv.load_dotenv()

motherduck_token = Secret.load("motheducktoken").get()
if not motherduck_token:
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")


# def get_connection():
#     duckdb_connector = DuckDBConnector(
#         database=f"md:?motherduck_token={motherduck_token}",
#     ).load("motherduck")  # blockname

#     return duckdb_connector


def get_connection():
    connection = duckdb.connect(f"md:?motherduck_token={motherduck_token}")
    return connection