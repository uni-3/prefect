start-server:
	prefect server start

register-duckdb:
	prefect block register -m prefect_duckdb

create-block:
	prefect block create duckdb-connector # -n LOCAL_DB

update-modal:
	uv run prefect work-pool update modal --base-job-template ./templates/modal_job_template.json

docker-push:
	docker push uni3san/modal-run:latest

docker-build:
	docker build . -t uni3san/modal-run:latest

docker-login:
	docker login