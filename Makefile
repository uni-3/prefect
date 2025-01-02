.PHONY: help
.DEFAULT_GOAL := help

start-server:
	prefect server start

register-duckdb:
	prefect block register -m prefect_duckdb

create-block:
	prefect block create duckdb-connector # -n LOCAL_DB

update-modal:
	uv run prefect work-pool update modal --base-job-template ./templates/modal_job_template.json

prefect-login:
	uv run prefect cloud login

deploy: ## deploy prefect flow
	uv run prefect deploy

docker-push:
	docker push uni3san/modal-run:latest

docker-build:
	docker build . -t uni3san/modal-run:latest

docker-login:
	docker login

run-dbt:
	cd dbt_project && uv run dbt run --target=prod

dbt-deps:
	cd dbt_project && uv run dbt deps

start-evidence: ## start evidence
	cd dbt_project/reports && docker compose up -d

help: ## helpです コマンドの後ろに説明を書くとコマンドと説明が表示されます
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
