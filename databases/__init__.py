#from prefect_duckdb.database import DuckDBConnector
from prefect_duckdb import DuckDBConnector
from prefect.variables import Variable
from prefect.blocks.system import Secret

import dotenv

import os
# .envファイルの内容を環境変数として読み込む
dotenv.load_dotenv()

secret_block = Secret.load("motheducktoken")
if not secret_block:
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
else:
    motherduck_token = secret_block.get()


def get_connection():
    duckdb_connector = DuckDBConnector(
        database=f"md:?motherduck_token={motherduck_token}",
    ).load("motherduck")  # blockname

    return duckdb_connector
