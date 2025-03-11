.PHONY: help
.DEFAULT_GOAL := help

start-server: ## start prefect server
	prefect server start

register-duckdb: ## register duckdb block
	prefect block register -m prefect_duckdb

create-block: ## create	duckdb connector
	prefect block create duckdb-connector # -n LOCAL_DB

update-modal: ## update modal work pool
	uv run prefect work-pool update modal --base-job-template ./templates/modal_job_template.json

prefect-login: ## login prefect cloud
	uv run prefect cloud login

deploy: ## deploy prefect flow
	uv run prefect deploy

docker-push: ## push docker image to docker hub
	docker push uni3san/modal-run:latest

docker-build: ## build docker image
	docker build . -t uni3san/modal-run:latest

docker-login: ## login docker hub
	docker login

run-dbt: ## run dbt with dbt_project
	cd dbt_project && uv run dbt run --target=prod

dbt-deps: ## install dbt deps
	cd dbt_project && uv run dbt deps

help: ## helpです コマンドの後ろに説明を書くとコマンドと説明が表示されます
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
