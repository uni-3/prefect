start-server:
	prefect server start

register-duckdb:
	prefect block register -m prefect_duckdb

create-block:
	prefect block create duckdb-connector # -n LOCAL_DB
